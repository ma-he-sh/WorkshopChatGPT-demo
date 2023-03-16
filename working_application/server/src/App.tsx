import React, { useState } from 'react';
import './styles/server.scss';
import { Button, Pane, Text, Alert, Label, Textarea, TextInputField } from 'evergreen-ui'

export default class App extends React.Component<{}, formStruct> {
  constructor(props:any) {
      super(props);
      this.state = {response: '', error_response: ''}
  }

  componentDidMount(): void {
    document.title = "ChatGPT-summary";
    document.documentElement.setAttribute("lang", 'en');
  }
  
  submitForm = (e:any) => {
      e.preventDefault();

      var data = {
        api_key:'',
        //site_url:'',
        chat_site_content: '',
        prompt: '',
      }

      if (e.target.hasOwnProperty('chat_api_key')) {
        data.api_key = e.target.chat_api_key.value;
      }

      // if (e.target.hasOwnProperty('chat_site_url')) {
      //   data.site_url = e.target.chat_site_url.value;
      // }

      if (e.target.hasOwnProperty('chat_site_content')) {
        data.chat_site_content = e.target.chat_site_content.value;
      }


      if (e.target.hasOwnProperty('chat_prompt')) {
        data.prompt = e.target.chat_prompt.value;
      }

      this.setState({error_response: ''});

      // fetch('/get_prompt', {
      fetch('/get_infor', {
        method: 'post',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data),
      } ).then((resp:any) => {
          return resp.json();
      }).then((data) => {
        if( data.payload ) {
          if( data.payload.success ) {
            this.setState({
              response:data.payload.response,
              error_response: '',
            });
          } else {
            console.log('error', data.payload.response);
            this.setState({error_response: data.payload.response});
          }
        }
      });
  }

  render() {
    console.log( this.state )
    return (
      <div id='app--window'>
        <div className='app--wrapper'>
          <form onSubmit={this.submitForm}>
            <TextInputField
              id="chat-api-key"
              label="Enter the API-KEY"
              required
              name='chat_api_key'
              placeholder="Enter API KEY"
              type="password"
            />
            {/* <TextInputField
              id="chat-website-url"
              label="Enter the website URL"
              required
              name='chat_site_url'
              placeholder="Enter Website URL"
            /> */}
            <Pane>
                <Label htmlFor="textarea-2" marginBottom={4} display="block">
                  Selected Content
                </Label>
                <Textarea id="chat_site_content" name='chat_site_content' placeholder="Enter Content" />
              </Pane>
            <Pane>
              <Label htmlFor="textarea-2" marginBottom={4} display="block">
                Enter Prompt
              </Label>
              <Textarea id="chat-prompt" name='chat_prompt' placeholder="Enter Prompt" />
            </Pane>
            <div className='chat-hr'></div>
            <Pane>
              <Button marginRight={16} appearance="primary">Submit</Button>
            </Pane>
          </form>
          {this.state.error_response.length > 0 && 
            <Pane>
              <div className='chat-hr'></div>
              <Alert
                intent="none"
                title={this.state.error_response}
                marginBottom={32}
              />
            </Pane>
          }
          <div className='chat-hr'></div>
          <Pane>
            <Textarea id="chat-prompt-response" readOnly={true} className="chat-prompt-response" value={this.state.response
            } />
          </Pane>
        </div>
      </div>
    )
  }
}

interface formStruct {
   [key:string]:any;
}