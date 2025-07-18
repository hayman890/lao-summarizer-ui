import streamlit as st
import boto3
import json

# Streamlit UI
st.set_page_config(page_title="Lao Summarizer", layout="centered")
st.title("Lao Summarizer")
st.write("Automatic summarization using SageMaker-deployed LLM.")

user_input = st.text_area("Enter Lao text to summarize", height=300)

if st.button("Summarize"):
    if not user_input.strip():
        st.warning("Please enter some Lao text.")
    else:
        with st.spinner("Summarizing..."):
            try:
                runtime = boto3.client(
                    "sagemaker-runtime",
                    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
                    region_name=st.secrets["AWS_REGION"]
                )

                payload = {
                    "inputs": user_input.strip()
                }

                response = runtime.invoke_endpoint(
                    EndpointName="lao-summarizer-endpoint",
                    ContentType="application/json; charset=utf-8",
                    Accept="application/json",
                    Body=json.dumps(payload)
                )

                body = response["Body"].read().decode("utf-8")
                result = json.loads(body)

                if isinstance(result, list) and "generated_text" in result[0]:
                    st.success("Summary:")
                    st.write(result[0]["generated_text"])
                else:
                    st.success("Summary:")
                    st.write(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")
