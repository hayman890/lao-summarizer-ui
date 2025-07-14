import streamlit as st
import boto3
import json

# Streamlit UI
st.set_page_config(page_title="Lao Summarizer", layout="centered")
st.title("Lao Summarizer")
st.write("Automatic summarization using SageMaker-deployed LLM.")

# Input box
user_input = st.text_area("Enter Lao text to summarize", height=300)

# Button
if st.button("Summarize"):
    if not user_input.strip():
        st.warning("Please enter some Lao text.")
    else:
        with st.spinner("Summarizing..."):
            try:
                # Connect to SageMaker endpoint
                runtime = boto3.client("sagemaker-runtime", region_name="ap-southeast-2")
                payload = {"inputs": user_input.strip()}
                response = runtime.invoke_endpoint(
                    EndpointName="lao-summarizer-endpoint",
                    ContentType="application/json",
                    Body=json.dumps(payload)
                )
                result = json.loads(response["Body"].read().decode("utf-8"))
                st.success("Summary:")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
