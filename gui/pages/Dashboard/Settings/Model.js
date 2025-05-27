import React, {useState, useEffect, useRef} from 'react';
import {ToastContainer, toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import agentStyles from "@/pages/Content/Agents/Agents.module.css";
import {storeApiKey, fetchApiKeys, validateLLMApiKey, fetchApiKey, storeLMStudio, verifyEndPoint} from "@/pages/api/DashboardService";
import {EventBus} from "@/utils/eventBus";
import {getUserClick, removeTab} from "@/utils/utils";
import Image from "next/image";

export default function Model({organisationId}) {
  const [temperature, setTemperature] = useState(0.5);
  const [models, setModels] = useState([
    {'name':'Open AI API key','logo':'/images/openai_logo.svg','source':'OpenAi', 'api_key': '', 'endpoint': ''},
    {'name':'Hugging Face auth token','logo':'/images/huggingface_logo.svg','source':'Hugging Face', 'api_key': '', 'endpoint': ''},
    {'name':'Replicate auth token','logo':'/images/replicate_logo.svg','source':'Replicate', 'api_key': '', 'endpoint': ''},
    {'name':'Google Palm API key','logo':'/images/google_palm_logo.svg','source':'Google Palm', 'api_key': '', 'endpoint': ''},
    {'name':'LM Studio','logo':'/images/lm_studio_logo.svg','source':'LM Studio', 'api_key': 'EMPTY', 'endpoint': 'http://192.168.0.144:1234', 'needsEndpoint': true}
  ]);
  const [updatedModels, setUpdatedModels] = useState([]);

  useEffect(() => {
    fetchApiKeys().then((response) => {
      if(response.data.length > 0) {
        response.data.forEach(item => {
          const index = models.findIndex(model => model.source.toLowerCase() === item.provider.toLowerCase());
          if (index !== -1) {
            const newModels = [...models];
            newModels[index].api_key = item.api_key;
            setModels(newModels);
          }
        });
      }
    })
  },[])

  const saveSettings = () => {
    updatedModels.forEach(model => {
      if (model.source === 'LM Studio') {
        // Handle LM Studio specially
        if (!model.endpoint || model.endpoint.replace(/\s/g, '') === '') {
          toast.error("LM Studio endpoint is required", {autoClose: 1800});
          return;
        }
        if (!model.api_key || model.api_key.replace(/\s/g, '') === '') {
          toast.error("LM Studio API key is required (use 'EMPTY' if no auth)", {autoClose: 1800});
          return;
        }

        // Verify endpoint first
        verifyEndPoint(model.api_key, model.endpoint, 'LM Studio')
          .then((response) => {
            if (response.data.success) {
              // Store LM Studio configuration
              storeLMStudio(model.api_key, model.endpoint)
                .then((response) => {
                  if (response.status === 200) {
                    getUserClick('LM Studio Configured', {'Endpoint': model.endpoint});
                    toast.success(`Successfully configured LM Studio at ${model.endpoint}`, {autoClose: 1800});
                  } else {
                    toast.error("Error configuring LM Studio", {autoClose: 1800});
                  }
                })
                .catch((error) => {
                  toast.error("Error configuring LM Studio", {autoClose: 1800});
                });
            } else {
              toast.error(`Cannot connect to LM Studio at ${model.endpoint}`, {autoClose: 1800});
            }
          })
          .catch((error) => {
            toast.error(`Error verifying LM Studio endpoint: ${error.message}`, {autoClose: 1800});
          });
      } else {
        // Handle other providers normally
        if (model.api_key === null || model.api_key.replace(/\s/g, '') === '') {
          toast.error("API key is empty", {autoClose: 1800});
          return;
        }
        validateLLMApiKey(model.source, model.api_key)
            .then((response) => {
              if (response.data.status === "success") {
                storeKey(model.source, model.api_key);
              } else {
                toast.error(`Invalid API key for ${model.source}`, {autoClose: 1800});
              }
            });
      }
    });
  };

  const storeKey = (model_provider, api_key) => {
    if(model_provider === 'OpenAi')
      model_provider = 'OpenAI'
    storeApiKey(model_provider,api_key).then((response) => {
      if(response.status === 200) {
        getUserClick('API Key Updated', {'Model': model_provider})
        toast.success(`Successfully Stored the API Key of ${model_provider}`, {autoClose: 1800})
      }
      else
        toast.error("Error", {autoClose: 1800})
    })
  }

  const handleInputChange = (source, value, field = 'api_key') => {
    const updatedModel = models.find(model => model.source === source);
    if (updatedModel) {
      updatedModel[field] = value;
      setUpdatedModels(prevModels => {
        const existingIndex = prevModels.findIndex(model => model.source === source);
        if (existingIndex !== -1) {
          return [
            ...prevModels.slice(0, existingIndex),
            updatedModel,
            ...prevModels.slice(existingIndex + 1)
          ];
        } else {
          return [...prevModels, updatedModel];
        }
      });
    }
  };

  useEffect(() => {
    console.log(updatedModels)
  },[updatedModels])

  const handleTemperatureChange = (event) => {
    setTemperature(event.target.value);
  };

  return (
      <>
        <div className="row">
          <div className="col-3"></div>
          <div className="col-6 col-6-scrollable">
            {models.map(model => (
                <div key={model.name}>
                  <div className="horizontal_container align_center mt_24 gap_8">
                    <Image width={16} height={16} src={model.logo} alt={`${model.name}-icon`} />
                    <span className="text_13 color_gray">{model.name}</span>
                  </div>
                  {model.needsEndpoint && (
                    <>
                      <input
                        placeholder="LM Studio Endpoint (e.g., http://192.168.0.144:1234)"
                        className="input_medium mt_8"
                        type="text"
                        value={model.endpoint}
                        onChange={(event) => handleInputChange(model.source, event.target.value, 'endpoint')}
                      />
                      <span className="text_12 color_gray mt_4">Enter your LM Studio server endpoint</span>
                    </>
                  )}
                  <input
                    placeholder={model.needsEndpoint ? "API Key (use 'EMPTY' for LM Studio)" : `Enter your ${model.name}`}
                    className="input_medium mt_8"
                    type={model.needsEndpoint ? "text" : "password"}
                    value={model.api_key}
                    onChange={(event) => handleInputChange(model.source, event.target.value, 'api_key')}
                  />
                  {model.needsEndpoint && (
                    <span className="text_12 color_gray mt_4">LM Studio doesn't require authentication - use 'EMPTY'</span>
                  )}
                </div>
            ))}
            {updatedModels.length > 0 && <div style={{display: 'flex', justifyContent: 'flex-end', marginTop: '15px'}}>
              <button onClick={() => removeTab(-3, "Settings", "Settings", 0)} className="secondary_button mr_10">Cancel</button>
              <button className="primary_button" onClick={saveSettings}>Update Changes</button>
            </div>}
          </div>
          <div className="col-3"></div>
        </div>
        <ToastContainer/>
      </>
  )
}