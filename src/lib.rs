use pyo3::prelude::*;

use ::atomic_counter as atomic_counter_rs;

pub use atomic_counter_rs::{Counter as RustCounter, TimeCounter as RustTimeCounter};

#[pyclass]
struct Counter(RustCounter);

#[pyclass]
struct TimeCounter(RustTimeCounter);

#[pymethods]
impl Counter {
    #[new]
    #[pyo3(signature = (base=None, now=None, interval=None))]
    fn new(base: Option<u64>, now: Option<u64>, interval: Option<u64>) -> Self {
        Counter(RustCounter::new(base, now, interval))
    }

    fn set(&mut self, val: u64) {
        self.0.set(val);
    }

    fn current(&self) -> u64 {
        self.0.current()
    }

    fn next(&mut self) -> u64 {
        self.0.next()
    }
}

#[pymethods]
impl TimeCounter {
    #[new]
    fn new() -> Self {
        TimeCounter(RustTimeCounter::new())
    }

    fn next(&mut self) -> u64 {
        self.0.next()
    }

    #[staticmethod]
    fn decode_timestamp_microseconds(value: u64) -> u64 {
        RustTimeCounter::decode_timestamp_microseconds(value)
    }

    fn current(&self) -> u64 {
        self.0.current()
    }
}

#[pymodule]
fn atomic_counter(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<Counter>()?;
    m.add_class::<TimeCounter>()?;
    Ok(())
}
