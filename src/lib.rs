use chrono::Utc;
use pyo3::prelude::*;
use std::sync::Mutex;

#[pyclass]
struct Counter {
    value: Mutex<u64>,
    interval: u64,
}

#[pyclass]
struct TimeCounter {
    value: Mutex<u64>,
}

// 2020-01-01
static _BASE: u64 = 1577854800000000000;

// For a timestamp with microsecond precision:
// - 52 bits for microseconds since epoch (covers ~142 years, expire 2112)
// - 12 bits for counter (4096 values per microsecond)
const MICROS_BITS: u32 = 52;
const COUNTER_BITS: u32 = 12;

const MICROS_MASK: u64 = (1 << MICROS_BITS) - 1;
const COUNTER_MASK: u64 = (1 << COUNTER_BITS) - 1;

#[pymethods]
impl Counter {
    #[new]
    fn new(base: Option<u64>, now: Option<u64>, interval: Option<u64>) -> Self {
        // now is the instantiation time of this
        let now = now.unwrap_or(Utc::now().timestamp_nanos() as u64);

        // base is either provided, or we use the default of 2020-01-01
        let base = base.unwrap_or(_BASE);

        Counter {
            value: Mutex::new(now - base),
            interval: interval.unwrap_or(1),
        }
    }

    fn set(&mut self, val: u64) {
        *self.value.lock().unwrap() = val;
    }

    fn current(&self) -> u64 {
        *self.value.lock().unwrap()
    }

    fn next(&mut self) -> u64 {
        *self.value.lock().unwrap() += self.interval;
        self.current()
    }
}

#[pymethods]
impl TimeCounter {
    #[new]
    fn new() -> Self {
        let mut counter = TimeCounter {
            value: Mutex::new(0),
        };
        {
            // Create a new scope for the mutex lock
            let mut val = counter.value.lock().unwrap();
            let now = Utc::now();
            let total_micros =
                (now.timestamp() as u64 * 1_000_000) + (now.timestamp_subsec_nanos() / 1000) as u64;
            let current_time_portion = (total_micros & MICROS_MASK) << COUNTER_BITS;
            // Using middle of range (4096/2) for creation
            // This is to defend against the unlikely case that the previous instance of this class
            // created an id with the same microsecond timestamp, so we stagger the first call
            // into the middle of the range.
            *val = current_time_portion | 2048;
        }
        counter
    }

    fn next(&mut self) -> u64 {
        let mut val = self.value.lock().unwrap();
        let now = Utc::now();

        // Calculate total microseconds since epoch
        let total_micros =
            (now.timestamp() as u64 * 1_000_000) + (now.timestamp_subsec_nanos() / 1000) as u64;

        // Construct the timestamp portion (52 bits microseconds + 12 bits counter)
        let current_time_portion = (total_micros & MICROS_MASK) << COUNTER_BITS;

        // If we're still in the same microsecond, increment counter
        // Otherwise, start at 0
        if (*val >> COUNTER_BITS) == (current_time_portion >> COUNTER_BITS) {
            let counter = (*val & COUNTER_MASK) + 1;
            if counter > COUNTER_MASK {
                panic!("Counter overflow - exceeded 4096 values in a single microsecond");
            } else {
                *val = current_time_portion | counter;
            }
        } else {
            *val = current_time_portion;
        }

        *val
    }

    #[staticmethod]
    fn decode_timestamp_microseconds(value: u64) -> u64 {
        value >> COUNTER_BITS
    }

    fn current(&self) -> u64 {
        *self.value.lock().unwrap()
    }
}

#[pymodule]
fn atomic_counter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Counter>()?;
    m.add_class::<TimeCounter>()?;
    Ok(())
}
