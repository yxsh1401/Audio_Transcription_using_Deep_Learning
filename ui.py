import gradio as gr
import whisper
from deep_translator import GoogleTranslator

# Transcription function for file upload
def transcribe_file(file):
    model = whisper.load_model("base")
    result = model.transcribe(file.name)
    return result["text"]

# Transcription function for microphone input
def transcribe_audio(audio):
    model = whisper.load_model("base")
    result = model.transcribe(audio)
    return result["text"]

# Translation function
def translate_text(text, target_lang):
    if not text:
        return "Please provide text to translate"
    try:
        translator = GoogleTranslator(source="auto", target=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"

# Create the Gradio interface with custom CSS
with gr.Blocks(title="Audio Transcription & Translation") as demo:

    # Add custom CSS using gr.Markdown
    gr.Markdown("""
        <style>
            /* Container background */
            .gradio-container {
                background-color: #d1e7ff;  /* Light blue background */
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
                font-family: Arial, sans-serif;
            }

            /* Header styling */
            .header {
                font-size: 40px;
                font-weight: bold;
                color: #007BFF;
                text-align: center;
                padding-bottom: 30px;
                text-transform: uppercase;
            }

            /* Footer styling */
            .footer {
                font-size: 14px;
                text-align: center;
                padding-top: 20px;
                color: gray;
            }

            /* Button styling */
            .gr-button {
                background-color: #007BFF;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }

            .gr-button:hover {
                background-color: #0056b3;
                cursor: pointer;
            }

            /* Dropdown styling */
            .gr-dropdown {
                background-color: #e7f3fe;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px;
                width: 150px;  /* Smaller width for dropdown */
                transition: background-color 0.3s ease;
            }

            .gr-dropdown:hover {
                background-color: #c9e3fe;
            }

            /* Textbox styling */
            .gr-textbox {
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
                transition: border 0.3s ease;
            }

            .gr-textbox:focus {
                border: 1px solid #007BFF;
            }

            /* Row and column layout for elements */
            .gr-row {
                display: flex;
                justify-content: space-between;
                gap: 20px;
            }

            .gr-column {
                flex: 1;
            }

            /* Animation for elements */
            .gr-button, .gr-dropdown, .gr-textbox {
                animation: fadeIn 0.5s ease-in-out;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
        </style>
    """)

    # Header Section
    gr.Markdown('<div class="header">Audio Transcription & Translation Tool</div>')

    with gr.Tabs():
        # Tab for file upload
        with gr.TabItem("File Upload"):
            gr.Markdown("#### Upload an Audio or Video File for Transcription")
            with gr.Row():
                file_input = gr.File(type="filepath", label="Upload Audio/Video File")
                file_button = gr.Button("Transcribe File", variant="primary", elem_id="file_button")

        # Tab for microphone input
        with gr.TabItem("Microphone Input"):
            gr.Markdown("#### Record your Speech for Transcription")
            with gr.Row():
                audio_input = gr.Audio(type="filepath", label="Record Audio")
                
            # Transcribe Speech button below the audio input
            audio_button = gr.Button("Transcribe Speech", variant="primary", elem_id="audio_button")

        # Side-by-side layout for transcription and translation
        gr.Markdown("### Transcription and Translation")
        with gr.Row():
            with gr.Column(scale=1, elem_id="transcription-column"):
                transcription = gr.Textbox(
                    label="Transcription", 
                    lines=6, 
                    placeholder="Your transcription will appear here...",
                    elem_id="transcription-box"
                )

            with gr.Column(scale=1, elem_id="translation-column"):
                translation_output = gr.Textbox(
                    label="Translation", 
                    lines=6, 
                    placeholder="Your translation will appear here...",
                    elem_id="translation-box"
                )
        
        # Separator
        gr.Markdown("---")
        
        # Translation Section
        gr.Markdown("### Translate Transcription")
        with gr.Row():
            # Select language dropdown above the translation box
            language_choice = gr.Dropdown(
                choices=["es", "fr", "de", "it", "ja", "ko", "zh-cn", "ru", "ar", "hi"],
                value="es",
                label="Select Target Language",
                info="Choose the language you want the text translated to.",
                elem_id="lang_choice"
            )
            translate_button = gr.Button("Translate", elem_id="translate_button")

    # Footer Section
    gr.Markdown('<div class="footer">Developed with ❤️ by [Your Name or Team]. All rights reserved.</div>')

    # Set up event handlers
    file_button.click(fn=transcribe_file, inputs=[file_input], outputs=transcription)
    audio_button.click(fn=transcribe_audio, inputs=[audio_input], outputs=transcription)
    translate_button.click(fn=translate_text, inputs=[transcription, language_choice], outputs=translation_output)

if __name__ == "__main__":
    demo.launch()
