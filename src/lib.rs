use chrono::Utc;
use pyo3::prelude::*;
use std::sync::Mutex;

#[pyclass]
struct Counter {
    value: Mutex<u64>,
    interval: u64,
}

// 2020-01-01
static _BASE: u64 = 1577854800000000000;

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

#[pymodule]
fn atomic_counter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Counter>()?;
    Ok(())
}
