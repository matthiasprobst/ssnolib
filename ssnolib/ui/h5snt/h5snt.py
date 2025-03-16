import streamlit as st

if "rdf_file" not in st.session_state:
    st.session_state.rdf_file = None
else:
    rdf_file = st.session_state.rdf_file

if "uploaded_snt" not in st.session_state:
    st.session_state.uploaded_snt = None
else:
    uploaded_snt = st.session_state.uploaded_snt

if "hdf5_file" not in st.session_state:
    st.session_state.hdf5_file = None
else:
    hdf5_file = st.session_state.hdf5_file

uploaded_snt = st.session_state.uploaded_snt
hdf5_file = st.session_state.hdf5_file
rdf_file = st.session_state.rdf_file
st.set_page_config(layout="wide")

# Streamlit UI
st.title("Semantically enrich Standard Names in a HDF5")

st.write("Upload an HDF5 file and a Standard Name Table. Hit Apply to semantically enrich the HDF5 file with "
         "standard names.")
st.info("The standard name table will be associated with the HDF5 file using the attribute 'standard_name_table'.")

# Upload buttons for HDF5 and RDF files
hdf5_file = st.file_uploader("Upload an HDF5 file", type=["h5", "hdf5", "hdf"])
if hdf5_file:
    st.toast("HDF5 file uploaded successfully.", icon="📤")
    st.session_state.hdf5_file = hdf5_file

rdf_file = st.file_uploader("Upload a Standard Name Table file", type=["json-ld", "jsonld", "ttl"])
if rdf_file:
    st.toast("Standard Name Table uploaded successfully.", icon="📤")
    st.session_state.rdf_file = rdf_file

with st.spinner("Loading the libraries..."):
    import h5py
    import pandas as pd

    from ssnolib import SSNO, StandardNameTable
    from ssnolib.ssno import parse_table

    try:
        import h5rdmtoolbox as h5tbx
    except ImportError:
        st.error("Please install the 'h5rdmtoolbox' package.")
        st.stop()


def update_standard_name_semantics(hdf_src, snt: StandardNameTable):
    errs = []
    updated_names = []
    with h5tbx.File(hdf_src, mode="r+") as _h5:
        if snt.label is not None:
            _h5.attrs["standard_name_table"] = snt.label
        else:
            _h5.attrs["standard_name_table"] = snt.id
        _h5.frdf["standard_name_table"].predicate = SSNO.usesStandardNameTable
        _h5.frdf["standard_name_table"].object = snt

        ds_names = _h5.get_dataset_names()
        for ds_path in ds_names:
            sn = _h5[ds_path].attrs.get("standard_name", None)
            if sn is not None:
                try:
                    found_sn = snt.get_standard_name(sn)
                    if found_sn:
                        updated_names.append((sn, found_sn.id))
                        _h5[ds_path].rdf["standard_name"].predicate = SSNO.hasStandardName
                        _h5[ds_path].rdf["standard_name"].object = found_sn
                except Exception as e:
                    errs.append((sn, e))
                    st.toast(f"Error updating standard name '{sn}': {str(e)}", icon="⚠️")
        _h5.flush()
    return updated_names, errs


def get_standard_names_from_hdf5(file):
    # Open the HDF5 file using h5py
    try:
        with h5py.File(file, 'r') as f:
            result = []

            # Iterate over all datasets in the file
            def check_standard_name(name, obj):
                if isinstance(obj, h5py.Dataset):
                    # Check if the 'standard_name' attribute exists
                    if 'standard_name' in obj.attrs:
                        result.append((name, obj.attrs['standard_name']))

            # Walk through all datasets and check for 'standard_name' attribute
            f.visititems(check_standard_name)
            return result
    except Exception as e:
        st.toast(f"Error processing HDF5 file: {str(e)}", icon="⚠️")
        return []


# Function to process the JSON-LD/TTL file (if required for some other purpose)
def upload_snt(file):
    try:
        st.toast("Processing Standard Name Table file...", icon="🔄")
        snt = parse_table(data=file.read(), fmt="json-ld")
        if snt.label is not None:
            st.toast(f"Standard Name Table '{snt.label}' successfully loaded.", icon="📤")
        else:
            st.toast(f"Standard Name Table '{snt.id}' successfully loaded.", icon="📤")
        return snt
    except Exception as e:
        st.toast(f"Error processing Standard Name Table file: {str(e)}", icon="⚠️")
        return ""


# Button to apply the function
if st.button("Apply"):
    with st.spinner("Processing ..."):

        if rdf_file is not None:
            if uploaded_snt is None:
                uploaded_snt = upload_snt(rdf_file)
            st.session_state.uploaded_snt = uploaded_snt
        else:
            st.toast("Please upload a JSON-LD or TTL file.", icon="⚠️")

        if rdf_file is not None and uploaded_snt is not None:
            if hdf5_file is not None:
                standard_names = get_standard_names_from_hdf5(hdf5_file)

                updated_names, err_names = update_standard_name_semantics(hdf5_file, uploaded_snt)
                st.write(hdf5_file)

                if hdf5_file is not None:
                    name, ext = hdf5_file.name.rsplit('.', 1)
                    st.download_button("Download Modified HDF5", hdf5_file, f"{name}_sn_enriched.{ext}")

                with h5tbx.File(hdf5_file, mode="r") as h5:
                    st.html(h5.hdfrepr.html_repr(group=h5, collapsed=True, preamble=None, chunks=False, maxshape=False))

                err_df = pd.DataFrame(err_names, columns=["Standard Name", "Error"])

                if len(err_names) > 0:
                    err_names_container = st.container()
                    err_names_container.write("These 'standard_name' could not be semantically updated:")
                    err_names_container.write(err_df)

                if len(updated_names) > 0:
                    updated_names_ds_container = st.container()
                    updated_names_ds = pd.DataFrame(updated_names, columns=["Standard Name (Attribute Value)", "URI"])
                    updated_names_ds_container.write("These 'standard_name' were semantically updated:")
                    updated_names_ds_container.write(updated_names_ds)

                # if standard_names:
                #     st.toast(f"Found {len(standard_names)} 'standard_name' attributes.", icon="ℹ️")
                #     st.toast(f"Displaying standard names in the table.", icon="ℹ️")
                #     df = pd.DataFrame(standard_names, columns=["Dataset path", "Standard Name (Attribute Value)"])
                #     st.table(df)
                # else:
                #     st.toast("No 'standard_name' attributes found in HDF5 file.", icon="⚠️")

            else:
                st.toast("Please upload an HDF5 file.")

if rdf_file is not None:
    container1 = st.container(border=True)
    if rdf_file is not None and uploaded_snt:
        if st.button("Display Standard Name Table"):
            container1 = st.container(border=True)
            container1.write("Standard Name Table:")
            container1.write(uploaded_snt)

            container2 = st.container(border=True)
            container2.code(uploaded_snt.serialize(format="ttl", structural=False), language="turtle")
