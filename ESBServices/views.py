import json
import datetime

from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import serializer as ser
from .models import CDAValidateModel


def exchange(data: list) -> dict:
    content = {}
    for item in data:
        content[item['DATA_ELEMENT_EN_NAME']] = None if item['DATA_ELEMENT_VALUE'] == '' else item['DATA_ELEMENT_VALUE']
    return content


# Create your views here.
@api_view(["POST"])
def verification(request):
    """
    平台服务字段级别校验工具
    :param request:
    :return:
    """
    content = json.loads(request.body)
    sevice_code = content.get("service").get("serviceCode")

    match sevice_code:
        #     检查申请单,状态更新
        case "S0041" | "S0042" | "S0061":
            # 病理检查状态,节点不同,需要单独处理
            if 'EXAM_APPLY' in content.get("message", {}).keys():
                message = exchange(content.get("message", {}).get("EXAM_APPLY", {}))
                serializer = ser.ExamApplySerializer(data=message)
            else:
                message = exchange(content.get("message", {}).get("PATHOLOGY_APPLY", {}))
                serializer = ser.PathologyApplySerializer(data=message)
            serializer.is_valid(raise_exception=True)

        case "S0023" | "S0024":
            # 挂号,退号
            message = exchange(content.get("message", {}).get("ENCOUNTER_OUTPATIENT", {}))
            serializer = ser.EncounterOutpatientSerializer(data=message)
            serializer.is_valid(raise_exception=True)

        case "S0044" | "S0045":
            # 病理申请
            message = exchange(content.get("message", {}).get("PATHOLOGY_APPLY", {}))
            serializer = ser.PathologyApplySerializer(data=message)
            serializer.is_valid(raise_exception=True)

        case "S0071" | "S0072":
            # 检查结果
            message = exchange(content.get("message", {}).get("EXAM_RESULT", {}))
            serializer = ser.ExamResultSerializer(data=message)
            serializer.is_valid(raise_exception=True)

        case "S0074" | "S0075":
            #  病理结果
            message = exchange(content.get("message", {}).get("PATHOLOGY_RESULT", {}))
            serializer = ser.PathologyResultSerializer(data=message)
            serializer.is_valid(raise_exception=True)

        case _:
            message = "本消息暂时未参与校验"

    data = {
        'message': message if isinstance(message, str) else "ok",
        "gmt_created": datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    }
    return Response(data)


class CDAValidateModelCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """用于校验CDA文档"""
    model = CDAValidateModel
    serializer_class = ser.CDAValidateModelSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


