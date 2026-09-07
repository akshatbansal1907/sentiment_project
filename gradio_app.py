import gradio as gr
from model import predict_sentiment


def predict(text):
    result = predict_sentiment(text)

    return (
        f"Sentiment: {result['label']}\n"
        f"Confidence: {result['confidence']:.3f}"
    )


demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(
        lines=5,
        placeholder="Enter a sentence or review..."
    ),
    outputs=gr.Textbox(),
    title="Sentiment Analysis",
    description="Enter text to determine whether the sentiment is positive or negative."
)

demo.launch(server_name="0.0.0.0", server_port=7860)
