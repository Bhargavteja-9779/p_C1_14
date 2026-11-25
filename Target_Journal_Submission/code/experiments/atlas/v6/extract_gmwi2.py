"""Extract coefficients of the published GMWI2 model (Chang et al. 2024, Nat Commun 15:7447; MIT licence; bioconda
gmwi2-1.6) WITHOUT executing arbitrary pickle code: joblib's unpickler restricted to a whitelist of classes."""
import sys, json, numpy as np, joblib.numpy_pickle as jp
ALLOWED = {("sklearn.linear_model._logistic", "LogisticRegression"), ("joblib.numpy_pickle", "NumpyArrayWrapper"),
           ("numpy", "ndarray"), ("_codecs", "encode"), ("numpy", "dtype"), ("numpy.core.multiarray", "_reconstruct"),
           ("numpy._core.multiarray", "_reconstruct"), ("numpy.core.multiarray", "scalar"), ("numpy._core.multiarray", "scalar")}
class Safe(jp.NumpyUnpickler):
    def find_class(self, module, name):
        if (module, name) not in ALLOWED: raise RuntimeError(f"blocked {module}.{name}")
        return super().find_class(module, name)
src, out = sys.argv[1], sys.argv[2]
with open(src, "rb") as f:
    m = Safe(src, f, ensure_native_byte_order=True).load()
coef = np.asarray(m.coef_).ravel(); names = list(m.feature_names_in_)
json.dump(dict(source="GMWI2 1.6 (bioconda), GMWI2_model.joblib", intercept=float(np.ravel(m.intercept_)[0]),
               C=m.C, penalty=m.penalty, classes=[str(c) for c in m.classes_],
               features=[n for n, c in zip(names, coef) if c != 0], coef=[float(c) for c in coef if c != 0], n_features_total=len(names)),
          open(out, "w"), indent=0)
print(len(names), (coef != 0).sum(), m.classes_, float(np.ravel(m.intercept_)[0])); print(names[:3]); print([n for n,c in zip(names,coef) if c!=0][:5])
