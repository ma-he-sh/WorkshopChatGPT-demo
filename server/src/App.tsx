import React, { useState } from 'react';
import './styles/server.scss';
import { Button, Pane, Text, Label, Textarea, TextInputField } from 'evergreen-ui'

export default class App extends React.Component<{}, formStruct> {
  componentDidMount(): void {
    document.title = "ChatGPT-summary";
    document.documentElement.setAttribute("lang", 'en');
  }
  
  render() {
    return (
      <div id='app--window'>
        <div className='app--wrapper'>
          <TextInputField
            id="chat-api-key"
            label="Enter the API-KEY"
            required
            placeholder="Enter API KEY"
            type="password"
          />
          <TextInputField
            id="chat-website-url"
            label="Enter the website URL"
            required
            placeholder="Enter Website URL"
          />
          <Pane>
            <Label htmlFor="textarea-2" marginBottom={4} display="block">
              Enter Prompt
            </Label>
            <Textarea id="chat-prompt" placeholder="Enter Prompt" />
          </Pane>
        </div>
      </div>
    )
  }
}

interface formStruct {
   [key:string]:any;
}