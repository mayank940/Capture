import streamlit as st

def style_base_layout():
    st.markdown("""
    <style> 
        @import url("https://googleapis.com");
            
        :root{
            --primary : #5A189A;
            --secondary : #7B2CBF;
            --accent :#C77DFF;
            --background : #F8F9FC;
            --card_background : #FFFFFF;
            --navbar : #240046;
            --text_primary : #1F2937;
            --text_secondary : #6B7280;
            --success : #22C55E;
            --warning : #F59E0B;
            --danger : #EF4444;
            --secondary_button_hover : #E0AAFF;
            --placeholder : #9CA3AF;
            --input_border : #D1D5DB;
        }

        header[data-testid="stHeader"]{
            display : none;
        }

        [data-testid="stAppViewContainer"]{
            background-color : var(--background);
        }

        h2{
            padding: 0 !important;
            color: var(--text_primary) !important;
            font-family: "Poppins", san-serif !important;
        }   
            
        h3{
            padding: 0 !important;
            color: var(--text_secondary) !important;
            font-family: "Poppins", san-serif !important;
        }   

        section[role="dialog"]{
            background-color : var(--card_background);
            border : 2px solid #E5E7EB;
            border-radius : 18px;
            color : #6B7280;
        }

        section[role="dialog"] h2 p{
            padding: 1rem;
            color : #1F2937;
        }
            
        button[aria-label="Close"]{
            color : #6B7280;
        }

        button[aria-label="Close"]:hover{
            color : #1F2937;
        }

        button, p{
            font-family: "Inter", san-serif !important;    
        }
            
        button[kind="primary"]{
            background-color: var(--primary);
            border-radius: 2rem;
            padding: 0.2rem 1rem;
            border: none;
            transform: translateY(2px);
            transition: transform 200ms ease-in-out, background-color 100ms ease-in, color 100ms ease-in;
        }
            
        button[kind="secondary"] {
            background-color: white;
            border: 2px solid var(--primary);
            color: var(--primary);
            border-radius: 2rem;
            padding: 0.2rem 1rem;
            transform: translateY(2px);
            transition: transform 250ms ease-in-out, background-color 150ms ease-in, color 150ms ease-in;
        }

        button[kind="tertiary"]{
            background-color: transparent;
            color: #6B7280;
            border: none;
            border-radius: 2rem;
            padding: 0.2rem 1.5rem;
            transfrom: translateY(2px);
            transition: background-color 250ms ease, color 250ms ease, box-shadow 250ms ease, transform 250ms ease;
        }
            
        button[kind="primary"]:hover{
            background-color: var(--secondary);
            transform: scale(1.02);
        }
                
        button[kind="secondary"]:hover {
            background-color: var(--secondary_button_hover);
            color: white;
            transform: scale(1.02);
        }

        button[kind="tertiary"]:hover{
            cursor: pointer;
            background-color: #F3F4F6;
            color: #5A189A;
            box-shadow: 2px 3px 8px  rgba(0, 0, 0, 0.2);
            transform: scale(1.02);
        }
            
        button div[data-testid="stMarkdownContainer"] p{
            font-size: 1.1rem;
            font-size: 900;
            }


        label[data-testid="stWidgetLabel"] p{
            color: var(--text_primary);
            font-size : 1rem;
            font-weight : 600;
        }

        div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] input{
            color: var(--text_primary);
            background-color: transparent;
        }
                
        div[data-testid="stTextInputRootElement"], div[data-testid="stSelectbox"] > div > div {
            background-color: var(--card_background);   
            border: 3px solid var(--input_border);
        }
                
        div[data-testid="stTextInput"] input::placeholder, div[data-testid="stSelectbox"] input::placeholder{
                color: var(--placeholder);
        }
                            
        div[data-testid="stTextInputRootElement"]:focus-within, div[data-testid="stSelectbox"] div[role="group"]:focus-within{
            border: 3px solid var(--secondary);
            box-shadow: 0 0 10px 3px rgba(123, 44, 191, 0.18);
        }
                  
        div[data-testid="stTextInputRootElement"] button{
            height: 100%;
            background-color: var(--secondary);
            border-radius: 5px 0 0 5px;
            padding: 0 1rem;        
        }

        div[data-testid="stSelectbox"] button svg{
            color: var(--secondary);
        }
                
        div[data-testid="stAlert"] div[role="status"]{
            background-color : #F0FDF4;
            border : 1px solid #BBF7D0;
            border-left : 4px solid #22C55E;
            color : #166534;
            //background-color: #DCFCE7;
            //color: #166534;        
        }

        div[data-testid="stAlert"] div[role="status"] span[data-testid="stAlertDynamicIcon"]{
            color : #22C55E;
        }
                
        div[data-testid="stAlert"] div[role="alert"]{
            background-color : #FEF2F2;
            border : 1px solid #FECACA;
            border-left : 4px solid #EF4444;
            color : #EF4444;

            //background-color: #FEF3C7;
            //color: #92400E;        
        }

        div[data-testid="stAlert"] div[role="alert"] span[data-testid="stAlertDynamicIcon"]{
            color : #EF4444;
        }

        div[data-testid="stAlert"] div:has(div[data-testid="stAlertContentInfo"]){
            background-color : var(--card-background);
            border: 1px solid #E5E7EB;
            border-left : 4px solid #7B2CBF;
            border-radius : 12px;
            box-shadow : 0 4px 12px rgba(36, 0, 70, 0.08);
            color : #6B7280;
        }

        div[data-testid="stAlert"] div:has(div[data-testid="stAlertContentInfo"]) span[data-testid="stAlertDynamicIcon"]{
            color : #7B2CBF;
        }

        div[data-testid="stProgress"] p{
            color : var(--text_primary);
            margin : 4px;
            font-weight : 400;
            font-size : 1rem;
        }

        div[data-testid="stProgressBarTrack"] > div{
            background-color : var(--secondary);
        }

        div[data-testid="stProgress"] div[data-testid="stProgressBarTrack"]{
            background-color : var(--card_background);
            box-shadow : 2px 2px 3px rgba(0, 0, 0, 0.1);
        }

        div[data-testid="stText"] span{
            color : var(--text_primary);
        }
     
        section[data-testid="stFileUploaderDropzone"]{
            border: 3px solid #D1D5DB;        
            background-color: var(--card_background);
        }
                
        div[data-testid="stFileUploaderDropzoneInstructions"] span{
            color: var(--text_secondary);        
            font-weight : 500;
            font-size : 1rem;
        }

        div[data-testid="stCameraInputWebcamComponent"]{
            padding: 1rem 0.8rem;
        }
                
        div[data-testid="stCameraInputWebcamStyledBox"]{
            overflow: hidden;
            border: 4px solid var(--secondary);        
            box-sizing: border-box;
            border-radius: 1rem;
            box-shadow: 2px 8px 10px rgba(0, 0, 0, 0.3);
        }
                
        div[data-testid="stCameraInputWebcamStyledBox"] video{
            width: 100%;
            background-color: transparent;
            padding: 0;
            height : 525px;
        }
                
        div[data-testid="stCaptionContainer"] p{
            color : var(--text_primary);
            opacity: 1;
            font-weight: 500;
        }
                
        button[data-testid="stCameraInputButton"]{
            background-color: white;
            border: 2px solid var(--primary);
            color: var(--primary);
            margin-top: 1.7rem;
            border-radius: 2rem;
            padding: 0.1rem 1rem;
            transform: translateY(2px);
            transition: transform 250ms ease-in-out;
        }
                
        button[data-testid="stCameraInputButton"]:hover{
            background-color: var(--secondary_button_hover);
            border: 2px solid var(--primary);
            color: white;
            transform: scale(1.02);        
        }

        hr{
            background-color: #D1D5DB !important;
        }
    </style>

    """, unsafe_allow_html=True)
