import xarray as xr

"""See https://docs.xarray.dev/en/stable/internals/extending-xarray.html"""


class XrSsnoAttrs:

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def __setitem__(self, key, value):
        self._obj.attrs[key] = value
        rdf_predicate = self._obj.attrs.get('RDF_PREDICATE', {})
        rdf_predicate[key] = value.model_dump_jsonld()
        self._obj.attrs['RDF_PREDICATE'] = rdf_predicate

    def __getitem__(self, item):
        return self._obj.attrs[item]
@xr.register_dataset_accessor("ssno")
class StandardNameAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def __call__(self, standard_name):
        for cname, coord in self._obj.coords.items():
            if standard_name == coord.attrs.get('standard_name', ''):
                return coord

    @property
    def attrs(self):
        return XrSsnoAttrs(self._obj)

