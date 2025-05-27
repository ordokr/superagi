from superagi.llms.hugging_face import HuggingFace
from superagi.llms.lm_studio import LMStudio

class ModelsHelper:
    @staticmethod
    def validate_end_point(model_api_key, end_point, model_provider):
        response = {"success": True}

        if (model_provider == 'Hugging Face'):
            try:
                result = HuggingFace(api_key=model_api_key, end_point=end_point).verify_end_point()
            except Exception as e:
                response['success'] = False
                response['error'] = str(e)
            else:
                response['result'] = result
        elif (model_provider == 'LM Studio'):
            try:
                lm_studio = LMStudio(api_key=model_api_key, end_point=end_point)
                result = lm_studio.verify_access_key()
                if not result:
                    response['success'] = False
                    response['error'] = 'Failed to connect to LM Studio endpoint'
                else:
                    response['result'] = {'status': 'connected', 'endpoint': end_point}
            except Exception as e:
                response['success'] = False
                response['error'] = str(e)

        return response


