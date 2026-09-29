import base64
import html
import os
import re

import requests
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 2rem;
}

.document-preview {
    background: #111827;
    color: #f9fafb;
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid #374151;
    max-height: 650px;
    overflow-y: auto;
    line-height: 1.7;
}

.doc-heading {
    font-size: 1.4rem;
    font-weight: 700;
    margin-top: 1.4rem;
    color: #ffffff;
}

.doc-section {
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 1.2rem;
    color: #e5e7eb;
}

.doc-paragraph {
    margin-bottom: 0.8rem;
}

.doc-bullet {
    margin-left: 1rem;
    margin-bottom: 0.4rem;
}

.doc-spacer {
    height: 0.5rem;
}

.warning-box {
    padding: 1rem;
    border-radius: 8px;
    background: #fff7ed;
    border: 1px solid #fed7aa;
    color: #7c2d12;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "generated" not in st.session_state:
    st.session_state.generated = False


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="subtitle">
AI-Powered Legal Document Drafting Assistant
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="warning-box">
<strong>Important:</strong>
LegalEase generates AI-assisted document drafts. It does not provide
legal advice. Review generated documents with a qualified legal
professional before signing or relying upon them.
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Document Settings")

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "Partnership Agreement",
            "General Contract",
            "Other",
        ],
    )

    if document_type == "Other":

        document_type = st.text_input(
            "Enter document type",
            placeholder="Example: Consulting Agreement",
        )

    st.divider()

    st.subheader("Branding")

    logo_file = st.file_uploader(
        "Upload optional logo",
        type=["png", "jpg", "jpeg"],
    )

    st.caption(
        "The logo will be included in DOCX/PDF exports."
    )

    st.divider()

    st.caption("Backend:")

    st.code(
        BACKEND_URL,
        language="text",
    )


# ============================================================
# MAIN FORM
# ============================================================

left, right = st.columns(
    [1, 1],
    gap="large",
)


# ============================================================
# LEFT SIDE - INPUT
# ============================================================

with left:

    st.subheader("Document Information")

    parties = st.text_area(
        "Parties Involved",
        height=150,
        placeholder=(
            "Example:\n"
            "Jane Doe (Employee)\n"
            "TechNova Inc. (Employer)"
        ),
    )

    terms = st.text_area(
        "Terms & Conditions",
        height=250,
        placeholder=(
            "Enter each term separated by a semicolon.\n\n"
            "Example:\n"
            "Monthly salary is ₹30,000; "
            "Salary will be paid on or before the 5th of every month; "
            "Employee shall perform assigned duties responsibly; "
            "Both parties shall maintain confidentiality; "
            "Either party may terminate the agreement with 30 days notice."
        ),
    )

    dates = st.text_input(
        "Effective Date",
        placeholder="Example: April 10, 2026",
    )

    generate_button = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# GENERATE DOCUMENT
# ============================================================

if generate_button:

    if not document_type.strip():

        st.error(
            "Please enter a document type."
        )

    elif not parties.strip():

        st.error(
            "Please provide the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please provide the terms and conditions."
        )

    elif not dates.strip():

        st.error(
            "Please provide the effective date."
        )

    else:

        payload = {
            "prompt": f"""
Create a professional {document_type}.

Parties involved:
{parties}

Terms and conditions:
{terms}

Effective date:
{dates}

Generate the complete legal document in a clear,
professional and well-structured format.
"""
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=300,
                )

                # ====================================================
                # SUCCESS RESPONSE
                # ====================================================

                if response.status_code == 200:

                    try:

                        result = response.json()

                    except ValueError:

                        st.error(
                            "Backend returned an invalid JSON response."
                        )

                        st.code(
                            response.text
                        )

                        result = None


                    if result is not None:

                        # ------------------------------------------------
                        # Accept multiple possible backend response keys
                        # ------------------------------------------------

                        generated_content = (
                            result.get("content")
                            or result.get("text")
                            or result.get("document")
                            or result.get("generated_text")
                            or result.get("output")
                        )

                        # ------------------------------------------------
                        # If backend directly returns a string
                        # ------------------------------------------------

                        if isinstance(result, str):

                            generated_content = result

                        # ------------------------------------------------
                        # Document found
                        # ------------------------------------------------

                        if generated_content:

                            st.session_state.document_text = str(
                                generated_content
                            )

                            st.session_state.generated = True

                            st.success(
                                "Document generated successfully."
                            )

                        # ------------------------------------------------
                        # No document found
                        # ------------------------------------------------

                        else:

                            st.error(
                                "Backend responded successfully, "
                                "but no generated document was found."
                            )

                            st.write(
                                "Backend response:"
                            )

                            st.json(result)

                # ====================================================
                # BACKEND ERROR
                # ====================================================

                else:

                    try:

                        error_data = response.json()

                        detail = error_data.get(
                            "detail",
                            error_data.get(
                                "message",
                                "Unknown backend error."
                            )
                        )

                    except Exception:

                        detail = response.text

                    st.error(
                        f"Generation failed "
                        f"(HTTP {response.status_code}): {detail}"
                    )

            # ========================================================
            # CONNECTION ERROR
            # ========================================================

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI."
                )

                st.info(
                    "Make sure the backend is running on: "
                    f"{BACKEND_URL}"
                )

            # ========================================================
            # TIMEOUT
            # ========================================================

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out."
                )

                st.info(
                    "Gemini may still be processing the request. "
                    "Please try again."
                )

            # ========================================================
            # GENERAL ERROR
            # ========================================================

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# ============================================================
# DOCUMENT PREVIEW / EDITOR
# ============================================================

with right:

    st.subheader(
        "Document Preview & Editor"
    )

    if st.session_state.generated:

        edited_text = st.text_area(
            "Edit your generated document",
            value=st.session_state.document_text,
            height=500,
        )

        st.session_state.document_text = edited_text

        st.markdown(
            "### Styled Preview"
        )

        escaped = html.escape(
            edited_text
        )

        preview_lines = []

        for line in escaped.splitlines():

            line = line.strip()

            # --------------------------------------------------------
            # Empty line
            # --------------------------------------------------------

            if not line:

                preview_lines.append(
                    '<div class="doc-spacer"></div>'
                )

            # --------------------------------------------------------
            # Numbered section
            # --------------------------------------------------------

            elif re.match(
                r"^\d+\.\s+",
                line,
            ):

                preview_lines.append(
                    f'<h3 class="doc-section">{line}</h3>'
                )

            # --------------------------------------------------------
            # Uppercase heading
            # --------------------------------------------------------

            elif (
                line.isupper()
                and len(line) < 120
            ):

                preview_lines.append(
                    f'<h2 class="doc-heading">{line}</h2>'
                )

            # --------------------------------------------------------
            # Bullet
            # --------------------------------------------------------

            elif line.startswith("- "):

                preview_lines.append(
                    '<div class="doc-bullet">'
                    f'• {line[2:]}</div>'
                )

            # --------------------------------------------------------
            # Normal paragraph
            # --------------------------------------------------------

            else:

                preview_lines.append(
                    f'<p class="doc-paragraph">{line}</p>'
                )

        st.markdown(
            '<div class="document-preview">'
            + "\n".join(preview_lines)
            + "</div>",
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "Your generated document will appear here."
        )


# ============================================================
# EXPORT SECTION
# ============================================================

if st.session_state.generated:

    st.divider()

    st.subheader(
        "Download Document"
    )

    export_cols = st.columns(3)


    # ========================================================
    # PREPARE LOGO
    # ========================================================

    logo_base64 = None

    if logo_file is not None:

        logo_bytes = logo_file.getvalue()

        logo_base64 = (
            "data:image/png;base64,"
            + base64.b64encode(
                logo_bytes
            ).decode("utf-8")
        )


    # ========================================================
    # EXPORT PAYLOAD
    # ========================================================

    export_payload = {
        "text": st.session_state.document_text,
        "document_type": document_type,
        "logo_base64": logo_base64,
    }


    # ========================================================
    # TXT EXPORT
    # ========================================================

    with export_cols[0]:

        if st.button(
            "Prepare TXT",
            use_container_width=True,
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/export/txt",
                    json=export_payload,
                    timeout=60,
                )

                if response.status_code == 200:

                    st.download_button(
                        "⬇️ Download TXT",
                        data=response.content,
                        file_name=(
                            f"{document_type.replace(' ', '_')}.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True,
                    )

                else:

                    st.error(
                        f"TXT export failed: "
                        f"{response.text}"
                    )

            except Exception as exc:

                st.error(
                    f"TXT export failed: {exc}"
                )


    # ========================================================
    # DOCX EXPORT
    # ========================================================

    with export_cols[1]:

        if st.button(
            "Prepare DOCX",
            use_container_width=True,
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/export/docx",
                    json=export_payload,
                    timeout=60,
                )

                if response.status_code == 200:

                    st.download_button(
                        "⬇️ Download DOCX",
                        data=response.content,
                        file_name=(
                            f"{document_type.replace(' ', '_')}.docx"
                        ),
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.wordprocessingml.document"
                        ),
                        use_container_width=True,
                    )

                else:

                    st.error(
                        f"DOCX export failed: "
                        f"{response.text}"
                    )

            except Exception as exc:

                st.error(
                    f"DOCX export failed: {exc}"
                )


    # ========================================================
    # PDF EXPORT
    # ========================================================

    with export_cols[2]:

        if st.button(
            "Prepare PDF",
            use_container_width=True,
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/export/pdf",
                    json=export_payload,
                    timeout=60,
                )

                if response.status_code == 200:

                    st.download_button(
                        "⬇️ Download PDF",
                        data=response.content,
                        file_name=(
                            f"{document_type.replace(' ', '_')}.pdf"
                        ),
                        mime="application/pdf",
                        use_container_width=True,
                    )

                else:

                    st.error(
                        f"PDF export failed: "
                        f"{response.text}"
                    )

            except Exception as exc:

                st.error(
                    f"PDF export failed: {exc}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "LegalEase | AI-assisted legal document drafting | "
    "Always obtain appropriate professional legal review."
)