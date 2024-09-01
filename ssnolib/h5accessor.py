try:
    from h5rdmtoolbox.wrapper.accessor import Accessor, register_accessor
    from h5rdmtoolbox.wrapper.core import Group
except ImportError:
    raise ImportError("h5rdmtoolbox is required for this function.")


@register_accessor("ssno", "group")
class SSNOAccessor(Accessor):
    """Accessor to await selected data to be converted to a new units"""

    def enrich_hdf(self,
                   standard_name_attribute="standard_name",
                   standard_name_table_attribute="standard_name_table") -> Group:
        """Add RDF information to an HDF5 file which has standard name attributes, i.e.
        datasets with a 'standard_name' attribute and the root group with a 'standard_name_table' attribute.

        Parameters
        ----------
        h5 : h5py.Group or str
            The root group of the HDF5 file or the filename of the HDF5 file.
        """
        h5 = self._obj  # root group

        # iteratively walk through the HDF5 file and add RDF information
        all_ds_with_sn = h5.find(flt={standard_name_attribute: {'$exists': True}}, objfilter='dataset')
        for ds in all_ds_with_sn:
            sn = ds.attrs[standard_name_attribute]
            h5[ds.name].rdf.predicate[
                standard_name_attribute] = "https://matthiasprobst.github.io/ssno#hasStandardName"

        snt_attr_val = h5.attrs.get(standard_name_table_attribute, None)
        if snt_attr_val is None:
            raise ValueError(f"Root group must have attribute '{standard_name_table_attribute}'")
        if not isinstance(snt_attr_val, str):
            raise ValueError(f"Attribute '{standard_name_table_attribute}' must be a string")
        if not snt_attr_val.startswith("http"):
            raise ValueError(f"Attribute '{standard_name_table_attribute}' must be a valid URI")
        h5.rdf.predicate[
            standard_name_table_attribute] = "https://matthiasprobst.github.io/ssno#hasStandardNameTable"
        h5.rdf.object[standard_name_table_attribute] = "https://matthiasprobst.github.io/ssno#StandardNameTable"
        return h5
