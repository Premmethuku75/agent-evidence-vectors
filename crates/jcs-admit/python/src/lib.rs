//! The native half of the `probityai` Python package.
//!
//! One extension module, `probityai._native`, carries the bindings. The Python
//! modules under `probityai` re-export its names; nothing here is meant to be
//! imported directly.
//!
//! Every refusal crosses the boundary with the native variant name and fields
//! unchanged, read from the crate's own `serde` serialization of its error, so a
//! Python caller branches on the same discriminant a Rust caller matches and the
//! npm package reports.

mod errors;
mod jcs_binding;

/// Native bindings for RFC 8785 admission (`jcs-admit`).
#[pyo3::pymodule]
mod _native {
    #[pymodule_export]
    use crate::errors::JcsError;

    #[pymodule_export]
    use crate::jcs_binding::{admit, admit_ijson, admit_with, is_canonical, is_canonical_with};

    use pyo3::prelude::*;

    #[pymodule_init]
    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add("DEFAULT_MAX_DEPTH", jcs_admit::DEFAULT_MAX_DEPTH)?;
        m.add("MAX_SUPPORTED_DEPTH", jcs_admit::MAX_SUPPORTED_DEPTH)?;
        m.add("DEFAULT_MAX_BYTES", jcs_admit::DEFAULT_MAX_BYTES)?;
        m.add("JCS_ADMIT_VERSION", crate::jcs_binding::BOUND_VERSION)?;
        Ok(())
    }
}
