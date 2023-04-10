use chrono::{DateTime, Utc};
use pyo3::prelude::*;
use std::sync::Mutex;

#[pyclass]
struct Counter {
    value: Mutex<u64>,
}

// 2010-01-01
static _BASE: i64 = 1262322000000000000;

fn dt_to_u64(dt: DateTime<Utc>, base: i64) -> u64 {
    (dt.timestamp_nanos() - base) as u64
}

#[pymethods]
impl Counter {
    #[new]
    fn new(offset: Option<u64>, base: Option<i64>) -> Self {
        // now is the instantiation time of this
        let now = Utc::now();

        // base is either provided, or we use the default of 2010-01-01
        let base = base.unwrap_or(_BASE);

        // offset is the difference between `now` and `base` in nanos.
        // offset is the offset from base to the start,'
        // e.g. start = base + offset
        let offset = offset.unwrap_or(dt_to_u64(now, base));

        Counter {
            value: Mutex::new(dt_to_u64(now, base) - offset),
        }
    }

    fn next(&mut self) -> u64 {
        let ret: u64 = *self.value.lock().unwrap();
        *self.value.lock().unwrap() += 1;
        ret
    }
}

#[pymodule]
fn atomic_counter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Counter>()?;
    Ok(())
}
