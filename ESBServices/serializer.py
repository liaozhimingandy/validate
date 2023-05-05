from rest_framework import serializers
from rest_framework.settings import api_settings
from .models import CDAValidateModel
from .utils import CDAUtils

list_CATEGORY = (("NOR", "普通申请单"), ("EDU", "教育/科研用途"), ("IDT", "日间患者申请单"))
list_sex = (
    ("0", "未知性别"),
    ("1", "男性"),
    ("2", "女性"),
    ("9", "未说明的性别")
)
list_EXAM_CATEGORY_CODE = (
    ("UIS", "超声"),
    ("RIS", "放射"),
    ("EIS", "内镜"),
    ("REIS", "电生理"),
    ("OIMS", "眼科检查")
)

list_APPLY_STATUS_CODE = (
    ('10', '待审核'),
    ('20', '已提交'),
    ('30', '已执行'),
    ('40', '已完成'),
    ('90', '停止/撤销'),
    ('1', '检查预约'),
    ('2', '取消检查预约'),
    ('3', '检查登记'),
    ('4', '取消检查登记'),
    ('5', '患者信息核对'),
    ('6', '图像采集'),
    ('7', '书写报告'),
    ('8', '检查审核'),
    ('9', '检查复审'),
    ('11', '打印报告')
)

list_MARITAL_STATUS_CODE = (
    ('10', '未婚'),
    ('20', '已婚'),
    ('21', '初婚'),
    ('22', '再婚'),
    ('23', '复婚'),
    ('30', '丧偶'),
    ('40', '离婚'),
    ('90', '未说明的婚姻状况')
)

# 挂号号别
list_REGISTER_CLINIC_TYPE_CODE = (
    (1, '普通门诊'),
    (2, '专科门诊'),
    (3, '专家门诊'),
    (4, '急诊门诊'),
    (5, '体检'),
)


class BaseSerializer(serializers.Serializer):
    """公共部分"""

    EMPI_ID = serializers.CharField(max_length=32, label='患者主索引号码', help_text="患者主索引号码",
                                    allow_blank=True, trim_whitespace=True)
    PK_PATIENT = serializers.CharField(max_length=64, trim_whitespace=True)
    ENCOUNTER_ID = serializers.CharField(max_length=64, trim_whitespace=True)
    ORG_CODE = serializers.CharField(max_length=18, allow_blank=True)
    ORG_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    ENCOUNTER_TYPE_CODE = serializers.CharField(max_length=32, trim_whitespace=True)
    ENCOUNTER_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    VISIT_ID = serializers.CharField(max_length=64, trim_whitespace=True)
    VISIT_NO = serializers.IntegerField(default=1, allow_null=True)
    PATIENT_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    GENDER_CODE = serializers.ChoiceField(list_sex)
    GENDER_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    DATE_OF_BIRTH = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                              allow_null=True)
    AGE_YEAR = serializers.IntegerField(max_value=200, default=0, allow_null=True)
    AGE_MONTH = serializers.IntegerField(max_value=12, default=0, allow_null=True)
    AGE_DAY = serializers.IntegerField(max_value=366, default=0, allow_null=True)
    AGE_HOUR = serializers.IntegerField(max_value=24, default=0, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate_PK_PATIENT(self, value):
        """校验PK_PATIENT"""
        if value.count("_") < 3:
            message = f"PK_PATIENT({value}) 校验不通过;规则为:院部代码_就诊类别_系统代码_患者编号"
            raise serializers.ValidationError(message)
        return value

    def validate_ENCOUNTER_ID(self, value):
        """校验ENCOUNTER_ID"""
        if value.count("_") < 3:
            message = f"ENCOUNTER_ID({value})校验不通过;规则：院部代码_就诊类别代码_系统代码_就诊流水号"
            raise serializers.ValidationError(message)
        return value


class ExamApplySerializer(BaseSerializer):
    """检查申请单信息校验"""

    VISIT_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",))
    DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True)
    DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    WARD_ID = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    WARD_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    BED_NO = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    EXAM_APPLY_ID = serializers.CharField(max_length=64, trim_whitespace=True)
    EXAM_APPLY_NO = serializers.CharField(max_length=32, trim_whitespace=True)
    PLACER_ORDER_NO = serializers.CharField(max_length=32, trim_whitespace=True)
    APPLY_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                allow_null=True)
    APPLY_DEPT_ID = serializers.CharField(max_length=64, trim_whitespace=True)
    APPLY_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    APPLY_DOCTOR_ID = serializers.CharField(max_length=32, trim_whitespace=True)
    APPLY_DOCTOR_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    DISEASE_DESC = serializers.CharField(max_length=512, allow_blank=True, trim_whitespace=True)
    PRESENT_HISTORY_DESC = serializers.CharField(max_length=512, allow_blank=True, allow_null=True,
                                                 trim_whitespace=True)
    DIAG_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                               allow_null=True)
    DIAG_CODE = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    DIAG_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    DIAG_DESC = serializers.CharField(max_length=512, allow_blank=True, trim_whitespace=True, allow_null=True)
    APPLY_PURPOSE_DESC = serializers.CharField(max_length=128, allow_blank=True, trim_whitespace=True, allow_null=True)
    EXAM_CATEGORY_CODE = serializers.ChoiceField(list_EXAM_CATEGORY_CODE)
    EXAM_CATEGORY_NAME = serializers.CharField(max_length=6, trim_whitespace=True)
    EXAM_CLASS_CODE = serializers.CharField(max_length=6, trim_whitespace=True)
    EXAM_CLASS_NAME = serializers.CharField(max_length=6, trim_whitespace=True)
    UNIVERSAL_SERVICE_CODE = serializers.CharField(max_length=32, trim_whitespace=True)
    UNIVERSAL_SERVICE_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    EXAM_PART_CODE = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    EXAM_PART_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    APPLY_CMMT = serializers.CharField(max_length=128, allow_blank=True, trim_whitespace=True, allow_null=True)
    SCHEDULE_START_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT,
                                                         input_formats=("%Y%m%dT%H%M%S",),
                                                         allow_null=True, default=None)
    SCHEDULE_END_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT,
                                                       input_formats=("%Y%m%dT%H%M%S",),
                                                       allow_null=True)
    REGISTRANT_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                     allow_null=True)
    REGISTRANT_OPERA_ID = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    REGISTRANT_OPERA_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True,
                                                  allow_null=True)
    CANCEL_FLAG = serializers.ChoiceField(choices=(0, 1), default=0)
    CANCEL_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                 allow_null=True)
    CANCEL_REASON_DESC = serializers.CharField(max_length=128, allow_blank=True, trim_whitespace=True, allow_null=True)
    CANCEL_OPERA_ID = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    CANCEL_OPERA_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    EXEC_ORG_CODE = serializers.CharField(min_length=18, max_length=18, trim_whitespace=True)
    EXEC_ORG_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    EXEC_SYSTEM_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True)
    EXEC_SYSTEM_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True)
    EXEC_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True)
    EXEC_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True)
    EMER_FLAG = serializers.ChoiceField(choices=(0, 1), default=0)
    GREEN_CHANNEL_FLAG = serializers.ChoiceField(choices=(0, 1), default=0)
    FEE_AMOUNT = serializers.DecimalField(max_digits=5, decimal_places=2, default=1, allow_null=True)
    APPLY_STATUS_CODE = serializers.ChoiceField(list_APPLY_STATUS_CODE)
    APPLY_STATUS_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True)
    GESTATION_WEEK = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True,
                                           default=None)
    GESTATION_DAY = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    LAST_MENSTRUAL_PERIOD = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True,
                                                  allow_null=True)
    EXEC_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                               allow_null=True)
    EXEC_OPERA_ID = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    EXEC_OPERA_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    CHARGE_QUANTITY = serializers.CharField(max_length=32, trim_whitespace=True, default=1, allow_null=True)
    AGE_MINUTE = serializers.IntegerField(max_value=60, allow_null=True)
    ON_ACCOUNT_ITEM_CODE = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True)
    ON_ACCOUNT_ITEM_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True)
    EXAM_DIRECTION_CODE = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    EXAM_DIRECTION_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    PRICE_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                allow_null=True)
    PRICE_OPERA_ID = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    PRICE_OPERA_NAME = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    OUTPATIENT_ID = serializers.CharField(max_length=32, trim_whitespace=True)
    INPATIENT_ID = serializers.CharField(max_length=32, allow_blank=True, trim_whitespace=True, allow_null=True)
    FROM_SRC = serializers.CharField(max_length=32, trim_whitespace=True)
    CATEGORY = serializers.ChoiceField(list_CATEGORY)
    ITEM_CODE = serializers.CharField(max_length=256, trim_whitespace=True, allow_null=True)
    ITEM_NAME = serializers.CharField(max_length=1024, trim_whitespace=True, allow_null=True)
    ITEM_INDEX = serializers.CharField(max_length=1024, trim_whitespace=True, allow_null=False,
                                       help_text="检查记录序号")

    def validate_EXAM_APPLY_ID(self, value):
        """校验EXAM_APPLY_ID"""
        if value.count("_") < 3:
            message = f"EXAM_APPLY_ID({value}) 校验不通过;规则：院部代码_就诊类别代码_系统代码_检查申请单号"
            raise serializers.ValidationError(message)
        return value

    def validate_ITEM_CODE(self, value):
        """校验组套信息"""
        if value and value.count("|") == 0:
            message = "多个明细使用|作为分隔符进行拼接"
            raise serializers.ValidationError(message)
        return value

    def validate_ITEM_NAME(self, value):
        """校验组套信息"""
        if value and value.count("|") == 0:
            message = "多个明细使用|作为分隔符进行拼接"
            raise serializers.ValidationError(message)
        return value

    def validate(self, attr):
        """其它校验"""
        # 如果作废,则取消时间等不能为空
        if all((attr["CANCEL_DATE_TIME"], attr["CANCEL_OPERA_ID"], attr["CANCEL_OPERA_NAME"],
                False if attr["CANCEL_FLAG"] else True)):
            message = "该申请单作废时,这些字段不能为空, CANCEL_DATE_TIME, EXEC_OPERA_ID, CANCEL_OPERA_NAME, CANCEL_FLAG"
            raise serializers.ValidationError(message)
        # 校验检查申请单状态,如果执行时间不为空,则执行相关字段必须不为空
        if len(attr['EXEC_DATE_TIME']) > 0:
            if len(attr['EXEC_OPERA_ID']) == 0 or len(attr['EXEC_OPERA_NAME']) == 0:
                message = "作为检查申请单执行时的消息,你的EXEC_DATE_TIME, EXEC_OPERA_ID, EXEC_OPERA_NAME三项必须合法"
                raise serializers.ValidationError(message)
        return attr


class EncounterOutpatientSerializer(BaseSerializer):
    """挂号信息校验"""

    MARITAL_STATUS_CODE = serializers.ChoiceField(list_MARITAL_STATUS_CODE)
    MARITAL_STATUS_NAME = serializers.CharField(max_length=10, trim_whitespace=True)
    PATIENT_RESOURCE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='病人来源代码',
                                                  allow_null=True)
    PATIENT_RESOURCE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='病人来源名称',
                                                  allow_null=True)
    PATIENT_TYPE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='病人类别代码',
                                              allow_null=True)
    PATIENT_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='病人类别名称',
                                              allow_null=True)
    SCHEDULE_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='排班表ID', allow_null=True)
    SCHEDULE_DATE = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                              allow_null=True)
    REGISTER_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                   allow_null=True)
    REGISTER_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号人ID', allow_null=True)
    REGISTER_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号人姓名',
                                                allow_null=True)
    REGISTER_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号科室代码', allow_null=True)
    REGISTER_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号科室名称',
                                               allow_null=True)
    REGISTER_DOCTOR_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号医师ID', allow_null=True)
    REGISTER_DOCTOR_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号医师姓名',
                                                 allow_null=True)
    REGISTER_AMPM_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号上下午代码',
                                               allow_null=True)
    REGISTER_AMPM_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号上下午名称',
                                               allow_null=True)
    REGISTER_CLINIC_TYPE_CODE = serializers.ChoiceField(list_REGISTER_CLINIC_TYPE_CODE, label='挂号号别代码')
    REGISTER_CLINIC_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号号别名称')
    REGISTER_REQ_TYPE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号号类代码',
                                                   allow_null=True)
    REGISTER_REQ_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号号类名称',
                                                   allow_null=True)
    REGISTER_SEQ_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号序号', allow_null=True)
    RESERVE_FLAG = serializers.ChoiceField(choices=(0, 1), label='预约标志')
    RESERVE_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='预约ID', allow_null=True)
    REGISTER_CHANNEL_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号渠道代码',
                                                  allow_null=True)
    REGISTER_CHANNEL_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='挂号渠道名称',
                                                  allow_null=True)
    RETURN_FLAG = serializers.ChoiceField(choices=(0, 1), label='退号标志')
    RETURN_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                 allow_null=True)
    RETURN_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='退号人ID', allow_null=True)
    RETURN_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='退号人姓名', allow_null=True)
    VISIT_TYPE_CODE = serializers.ChoiceField(choices=(1, 2), label='初诊标志代码')
    VISIT_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='初诊标志名称')
    VISIT_DEPT_ID = serializers.CharField(max_length=4, trim_whitespace=True, label='就诊科室代码', allow_null=True)
    VISIT_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊科室名称', allow_null=True)
    VISIT_START_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                      allow_null=True)
    VISIT_END_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                    allow_null=True)
    DOCTOR_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊医师ID', allow_null=True)
    DOCTOR_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊医师姓名', allow_null=True)
    THERAPY_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='疗法代码', allow_null=True)
    THERAPY_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='疗法名称（西医、中医、中西医结合）',
                                         allow_null=True)
    DIAG_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                               allow_null=True)
    DIAG_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='疾病诊断编码', allow_null=True)
    DIAG_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='诊断名称', allow_null=True)
    DIAG_DESC = serializers.CharField(max_length=32, trim_whitespace=True, label='诊断描述', allow_null=True)
    CLINIC_ROOM_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊诊室代码', allow_null=True)
    CLINIC_ROOM_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊诊室名称', allow_null=True)
    VISIT_STATUS_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊状态代码',
                                              allow_null=True)
    VISIT_STATUS_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='就诊状态名称',
                                              allow_null=True)
    ACCOUNT_TYPE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='结算类型代码',
                                              allow_null=True)
    ACCOUNT_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='结算类型名称',
                                              allow_null=True)
    AGE_MINUTE = serializers.CharField(max_length=32, trim_whitespace=True, label='年龄-分', allow_null=True)
    CESAREAN_SECTION_FLAG = serializers.ChoiceField(choices=(0, 1), label='剖宫产标识')
    SCHEDULE_TIME_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='排班时段ID', allow_null=True)
    RESERVE_SOURCE_ID = serializers.CharField(min_length=4, max_length=32, trim_whitespace=True, label='号源ID',
                                              allow_null=True)
    OUTPATIENT_ID = serializers.CharField(min_length=4, max_length=32, trim_whitespace=True, label='门急诊号标识',
                                          allow_null=True)

    def validate(self, attr):
        """其它校验"""
        # 如果作废,则取消时间等不能为空
        if attr["RETURN_FLAG"]:
            if not all((attr["RETURN_OPERA_ID"], attr["RETURN_DATE_TIME"], attr["RETURN_OPERA_NAME"])):
                message = "该申请单非作废时,这些字段不能为空, RETURN_OPERA_ID, RETURN_DATE_TIME, RETURN_OPERA_NAME"
                raise serializers.ValidationError(message)
        else:
            if any((attr["RETURN_OPERA_ID"], attr["RETURN_DATE_TIME"], attr["RETURN_OPERA_NAME"])):
                message = "该申请单作废时,这些字段为空, RETURN_OPERA_ID, RETURN_DATE_TIME, RETURN_OPERA_NAME"
                raise serializers.ValidationError(message)
        return attr


class PathologyApplySerializer(BaseSerializer):
    VISIT_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                label='就诊日期时间', help_text='就诊日期时间')
    DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='科室ID',
                                    help_text='科室ID')
    DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='科室名称',
                                      help_text='科室名称')
    WARD_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='病区ID',
                                    help_text='病区ID')
    WARD_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='病区名称',
                                      help_text='病区名称')
    BED_NO = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='床号', help_text='床号')
    PATHOLOGY_APPLY_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='病理申请ID',
                                               help_text='病理申请ID')
    PATHOLOGY_APPLY_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='病理申请单号',
                                               help_text='病理申请单号')
    PLACER_ORDER_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='医嘱号', help_text='医嘱号')
    APPLY_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                label='申请日期时间', help_text='申请日期时间')
    APPLY_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='申请科室ID',
                                          help_text='申请科室ID')
    APPLY_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='申请科室名称',
                                            help_text='申请科室名称')
    APPLY_DOCTOR_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='申请医师ID',
                                            help_text='申请医师ID')
    APPLY_DOCTOR_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='申请医师姓名',
                                              help_text='申请医师姓名')
    DISEASE_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='病情描述',
                                         help_text='病情描述')
    PRESENT_HISTORY_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                 label='现病史描述', help_text='现病史描述')
    DIAG_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                               label='诊断日期时间', help_text='诊断日期时间')
    DIAG_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='疾病诊断编码',
                                      help_text='疾病诊断编码')
    DIAG_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='诊断名称',
                                      help_text='诊断名称')
    DIAG_DESC = serializers.CharField(max_length=128, trim_whitespace=True, allow_null=True, label='诊断描述',
                                      help_text='诊断描述')
    APPLY_PURPOSE_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                               label='检查目的描述', help_text='检查目的描述')
    PATHOLOGY_CATEGORY_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                    label='病理分类代码', help_text='病理分类代码')
    PATHOLOGY_CATEGORY_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                    label='病理分类名称', help_text='病理分类名称')
    PATHOLOGY_CLASS_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                 label='病理类别代码', help_text='病理类别代码')
    PATHOLOGY_CLASS_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                 label='病理类别名称', help_text='病理类别名称')
    UNIVERSAL_SERVICE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='医嘱项目代码',
                                                   help_text='医嘱项目代码')
    UNIVERSAL_SERVICE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='医嘱项目名称',
                                                   help_text='医嘱项目名称')
    PATHOLOGY_PART_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                label='病理部位代码', help_text='病理部位代码')
    PATHOLOGY_PART_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                label='病理部位名称', help_text='病理部位名称')
    BIOPSY_SITE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='活检部位代码',
                                             help_text='活检部位代码')
    BIOPSY_SITE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='活检部位名称',
                                             help_text='活检部位名称')
    APPLY_CMMT = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='申请单备注',
                                       help_text='申请单备注')
    CLINIC_EXAM_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='临床检查描述',
                                             help_text='临床检查描述')
    SURGERY_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                  label='手术/操作日期时间', help_text='手术/操作日期时间')
    SURGERY_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='手术/操作代码',
                                         help_text='手术/操作代码')
    SURGERY_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='手术/操作名称',
                                         help_text='手术/操作名称')
    FIXATIVE_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                   label='固定时间', help_text='固定时间')
    FIXATIVE_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='固定医师ID',
                                              help_text='固定医师ID')
    FIXATIVE_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                label='固定医师姓名', help_text='固定医师姓名')
    FIXATIVE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='固定液代码',
                                          help_text='固定液代码')
    FIXATIVE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='固定液名称',
                                          help_text='固定液名称')
    SPECIMEN_TYPE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                               label='标本类型代码', help_text='标本类型代码')
    SPECIMEN_TYPE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                               label='标本类型名称', help_text='标本类型名称')
    SPECIMEN_NO = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='标本号',
                                        help_text='标本号')
    COLLECT_METHOD_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                label='采集方式代码', help_text='采集方式代码')
    COLLECT_METHOD_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                label='采集方式名称', help_text='采集方式名称')
    COLLECT_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                  label='采样日期时间', help_text='采样日期时间')
    COLLECT_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='采样科室ID',
                                            help_text='采样科室ID')
    COLLECT_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                              label='采样科室名称', help_text='采样科室名称')
    COLLECT_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='采样医师ID',
                                             help_text='采样医师ID')
    COLLECT_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                               label='采样医师姓名', help_text='采样医师姓名')
    DELIVERY_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                   label='送检日期时间', help_text='送检日期时间')
    DELIVERY_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='送检人ID',
                                              help_text='送检人ID')
    DELIVERY_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                label='送检医师姓名', help_text='送检医师姓名')
    RECEIVE_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                  label='接收日期时间', help_text='接收日期时间')
    RECEIVE_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='接收人ID',
                                             help_text='接收人ID')
    RECEIVE_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                               label='接收医师姓名', help_text='接收医师姓名')
    CANCEL_FLAG = serializers.ChoiceField(choices=(0, 1), label='作废标志', help_text='作废标志')
    CANCEL_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                 label='取消日期时间', help_text='取消日期时间', allow_null=True)
    CANCEL_REASON_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                               label='撤销原因描述', help_text='撤销原因描述')
    CANCEL_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='撤销人ID',
                                            help_text='撤销人ID')
    CANCEL_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='撤销人姓名',
                                              help_text='撤销人姓名')
    EXEC_ORG_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                          label='执行机构/院部代码', help_text='执行机构/院部代码')
    EXEC_ORG_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                          label='执行机构/院部名称', help_text='执行机构/院部名称')
    EXEC_SYSTEM_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='执行系统代码',
                                             help_text='执行系统代码')
    EXEC_SYSTEM_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='执行系统名称',
                                             help_text='执行系统名称')
    EXEC_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='执行科室ID',
                                         help_text='执行科室ID')
    EXEC_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='执行科室名称',
                                           help_text='执行科室名称')
    EMER_FLAG = serializers.ChoiceField(choices=(0, 1), allow_null=True, label='紧急标志',
                                        help_text='紧急标志')
    FEE_AMOUNT = serializers.DecimalField(max_digits=9, decimal_places=2, label='费用金额', help_text='费用金额',
                                          min_value=0)
    APPLY_STATUS_CODE = serializers.ChoiceField(list_APPLY_STATUS_CODE, label='申请单状态代码',
                                                help_text='申请单状态代码')
    APPLY_STATUS_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                              label='申请单状态名称', help_text='申请单状态名称')
    GESTATION_WEEK = serializers.IntegerField(max_value=4, allow_null=True, label='孕周-周',
                                              help_text='孕周-周')
    GESTATION_DAY = serializers.IntegerField(max_value=31, allow_null=True, label='孕周-天', help_text='孕周-天')
    LAST_MENSTRUAL_PERIOD = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                  label='末次月经', help_text='末次月经')
    SPECIMEN_QUANTITY = serializers.IntegerField(max_value=100, allow_null=True, label='术后送标本件数',
                                                 help_text='术后送标本件数')
    SURGERY_FINDING_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='手术所见',
                                                 help_text='手术所见')
    OUTGOING_FLAG = serializers.ChoiceField(choices=(0, 1), allow_null=True, label='外送标识', help_text='外送标识')
    OUTGOING_ORG_CODE = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                              label='外送机构代码', help_text='外送机构代码')
    OUTGOING_ORG_NAME = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                              label='外送机构名称', help_text='外送机构名称')
    RAPID_PARAFFIN_FLAG = serializers.ChoiceField(choices=(0, 1), allow_null=True, label='快速石蜡标识',
                                                  help_text='快速石蜡标识')
    AGE_MINUTE = serializers.IntegerField(max_value=60, allow_null=True, label='年龄-分', help_text='年龄-分')
    PATHOLOGY_NO = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='病理号',
                                         help_text='病理号')
    DELIVERY_SPECIMEN = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='送检标本',
                                              help_text='送检标本')
    CLINIC_FINDING_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='临床所见',
                                                help_text='临床所见')
    MENOPAUSE_FLAG = serializers.ChoiceField(choices=(0, 1), allow_null=True, label='绝经标识', help_text='绝经标识')
    CYTOLOGY_NO = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='细胞学编号',
                                        help_text='细胞学编号')
    INFECTIOUS_SPECIMEN_FLAG = serializers.ChoiceField(choices=(0, 1), allow_null=True, label='传染性标本标识',
                                                       help_text='传染性标本标识')
    INFECTIOUS_SPECIMEN_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                     label='传染性标本描述', help_text='传染性标本描述')
    PAST_PATHOLOGY_NO = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='既往病理号',
                                              help_text='既往病理号')
    PAST_PATHOLOGY_DIAG_DESC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True,
                                                     label='既往病理诊断', help_text='既往病理诊断')
    OUTPATIENT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='门急诊号标识',
                                          help_text='门急诊号标识')
    INPATIENT_ID = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='住院号标识',
                                         help_text='住院号标识')
    FROM_SRC = serializers.CharField(max_length=32, trim_whitespace=True, allow_null=True, label='数据来源系统',
                                     help_text='数据来源系统')
    CATEGORY = serializers.ChoiceField(list_CATEGORY, label='医嘱用途分类', help_text='医嘱用途分类')

    def validate_PATHOLOGY_APPLY_ID(self, value):
        """PATHOLOGY_APPLY_ID"""
        if value.count("_") < 3:
            message = f"PATHOLOGY_APPLY_ID->({value}) 校验不通过;规则：院部代码_就诊类别代码_系统代码_检查申请单号"
            raise serializers.ValidationError(message)
        return value

    def validate(self, attrs):
        """其它校验"""
        # 如果作废,则取消时间等不能为空
        if attrs["CANCEL_FLAG"]:
            if not all((attrs["CANCEL_OPERA_ID"], attrs["CANCEL_DATE_TIME"], attrs["CANCEL_OPERA_NAME"])):
                message = "该申请单非作废时,这些字段不能为空, CANCEL_OPERA_ID, CANCEL_OPERA_NAME, CANCEL_DATE_TIME"
                raise serializers.ValidationError(message)
        else:
            if any((attrs["CANCEL_OPERA_ID"], attrs["CANCEL_DATE_TIME"], attrs["CANCEL_OPERA_NAME"])):
                message = "该申请单作废时,这些字段为空, CANCEL_OPERA_ID, CANCEL_OPERA_NAME, CANCEL_DATE_TIME"
                raise serializers.ValidationError(message)
        return attrs


class ExamResultSerializer(BaseSerializer):
    """检查报告"""
    DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='科室ID', help_text='科室ID',
                                    allow_null=True)
    DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='科室名称', help_text='科室名称',
                                      allow_null=True)
    WARD_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='病区ID', help_text='病区ID',
                                    allow_null=True)
    WARD_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='病区名称', help_text='病区名称',
                                      allow_null=True)
    BED_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='床号', help_text='床号', allow_null=True)
    EXAM_RESULT_ID = serializers.CharField(max_length=128, trim_whitespace=True, label='检查报告ID',
                                           help_text='检查报告ID')
    FILLER_ORDER_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='报告单号', help_text='报告单号')
    EXAM_APPLY_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='检查申请ID',
                                          help_text='检查申请ID')
    EXAM_APPLY_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='检查申请单号',
                                          help_text='检查申请单号', allow_null=True)
    PLACER_ORDER_NO = serializers.CharField(max_length=32, trim_whitespace=True, label='医嘱号', help_text='医嘱号')
    APPLY_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                label='申请日期时间', help_text='申请日期 时间', allow_null=True)
    APPLY_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='申请科室ID',
                                          help_text='申请科室ID', allow_null=True)
    APPLY_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='申请科室名称',
                                            help_text='申请科室 名称', allow_null=True)
    APPLY_DOCTOR_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='申请医师ID',
                                            help_text='申请医师ID', allow_null=True)
    APPLY_DOCTOR_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='申请医师姓名',
                                              help_text='申请医师姓名', allow_null=True)
    DIAG_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                               label='诊断日期时间', help_text='诊断日期时间', allow_null=True)
    DIAG_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='疾病诊断编码',
                                      help_text='疾病诊断编码', allow_null=True)
    DIAG_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='诊断名称', help_text='诊断名称',
                                      allow_null=True)
    DIAG_DESC = serializers.CharField(max_length=32, trim_whitespace=True, label='诊断描述', help_text='诊断描述',
                                      allow_null=True)
    APPLY_PURPOSE_DESC = serializers.CharField(max_length=32, trim_whitespace=True, label='检查目的描述',
                                               help_text='检查目的描述', allow_null=True)
    EXAM_CATEGORY_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='检查分类代码',
                                               help_text='检查分类代码', allow_null=True)
    EXAM_CATEGORY_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='检查分类名称',
                                               help_text='检查分类名称', allow_null=True)
    EXAM_CLASS_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='检查类别代码',
                                            help_text='检查类别代码', allow_null=True)
    EXAM_CLASS_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='检查类别名称',
                                            help_text='检查类别名称', allow_null=True)
    UNIVERSAL_SERVICE_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='医嘱项目代码',
                                                   help_text='医嘱项目代码')
    UNIVERSAL_SERVICE_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='医嘱项目名称',
                                                   help_text='医嘱项目名称')
    EXAM_PART_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='检查部位代码',
                                           help_text='检查部位代码', allow_null=True)
    EXAM_PART_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='检查部位名称',
                                           help_text='检查部位名称', allow_null=True)
    EXAM_FINDING_DESC = serializers.CharField(max_length=32, trim_whitespace=True, label='检查所见',
                                              help_text='检查所见', allow_null=True)
    EXAM_DIAG_DESC = serializers.CharField(max_length=32, trim_whitespace=True, label='诊断意见', help_text='诊断意见',
                                           allow_null=True)
    EXAM_SUGGESTION_DESC = serializers.CharField(max_length=1024, trim_whitespace=True, label='报告建议',
                                                 help_text='报告建议', allow_null=True)
    EXAM_RESULT_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='检查结果代码',
                                             help_text='检查结果代码', allow_null=True)
    EXAM_RESULT = serializers.CharField(max_length=32, trim_whitespace=True, label='检查定量结果',
                                        help_text='检查定量结果', allow_null=True)
    EXAM_RESULT_UNIT = serializers.CharField(max_length=32, trim_whitespace=True, label='检查定量结果计量单位',
                                             help_text='检查定量结果计量单位', allow_null=True)
    EXEC_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                               label='执行日期时间', help_text='执行日期时间', allow_null=True)
    EXEC_ORG_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='执行机构/院部代码',
                                          help_text='执行机构/院部代码', allow_null=True)
    EXEC_ORG_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='执行机构/院部名称',
                                          help_text='执行机构/院部名称', allow_null=True)
    EXEC_DEPT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='执行科室ID',
                                         help_text='执行科室ID', allow_null=True)
    EXEC_DEPT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='执行科室名称',
                                           help_text='执行科室名称', allow_null=True)
    EXEC_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='执行人ID', help_text='执行人ID',
                                          allow_null=True)
    EXEC_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='执行人姓名',
                                            help_text='执行人姓名', allow_null=True)
    REPORT_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                 label='报告日期时间', help_text='报告日期时间')
    REPORT_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='报告人ID', help_text='报告人ID')
    REPORT_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='报告医师姓名',
                                              help_text='报告医师姓名')
    CHECK_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                label='审核日期时间', help_text='审核日期时间', allow_null=True)
    CHECK_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='审核人ID', help_text='审核人ID',
                                           allow_null=True)
    CHECK_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='审核人姓名',
                                             help_text='审核人姓名', allow_null=True)
    REVIEW_DATE_TIME = serializers.DateTimeField(format=api_settings.TIME_FORMAT, input_formats=("%Y%m%dT%H%M%S",),
                                                 label='复审日期时间', help_text='复审日期时间', allow_null=True)
    REVIEW_OPERA_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='复审人ID', help_text='复审人ID',
                                            allow_null=True)
    REVIEW_OPERA_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='复审人姓名',
                                              help_text='复审人姓名', allow_null=True)
    EQUIPMENT_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='设备代码', help_text='设备代码',
                                           allow_null=True)
    EQUIPMENT_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='设备名称', help_text='设备名称',
                                           allow_null=True)
    REPORT_STATUS_CODE = serializers.CharField(max_length=32, trim_whitespace=True, label='报告单状态代码',
                                               help_text='报告单状态代码', allow_null=True)
    REPORT_STATUS_NAME = serializers.CharField(max_length=32, trim_whitespace=True, label='报告单状态名称',
                                               help_text='报告单状态名称', allow_null=True)
    WARN_FLAG = serializers.ChoiceField(choices=(0, 1), label='危急值标识', help_text='危急值标识', allow_null=True)
    DOCUMENT_CONTENT_PDF = serializers.CharField(max_length=256, trim_whitespace=True, label='文书内容_PDF',
                                                 help_text='文书内容_PDF', allow_null=True)
    CA_HASH = serializers.CharField(max_length=1024, trim_whitespace=True, label='CA数字签名hash值',
                                    help_text='CA数字签名hash值', allow_null=True)
    DOCUMENT_CONTENT_PDF_URL = serializers.CharField(max_length=32, trim_whitespace=True, label='文书PDF存放地址',
                                                     help_text='文书PDF存放地址', allow_null=True)
    AGE_MINUTE = serializers.IntegerField(max_value=100, label='年龄-分', help_text='年龄-分', allow_null=True)
    REPORT_TYPE = serializers.CharField(max_length=32, trim_whitespace=True, label='报告属性', help_text='报告属性',
                                        allow_null=True)
    DOCUMENT_CONTENT_CDA = serializers.CharField(max_length=32, trim_whitespace=True, label='文书内容_CDA',
                                                 help_text='文书内容_CDA', allow_null=True)
    OUTPATIENT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='门急诊号标识',
                                          help_text='门急诊号标识', allow_null=True)
    INPATIENT_ID = serializers.CharField(max_length=32, trim_whitespace=True, label='住院号标识',
                                         help_text='住院号标识', allow_null=True)

    def validate_EXAM_RESULT_ID(self, value):
        """PATHOLOGY_APPLY_ID"""
        if value.count("_") < 3:
            message = f"EXAM_RESULT_ID->({value}) 校验不通过;规则：院部代码_就诊类别代码_系统代码_检查报告号"
            raise serializers.ValidationError(message)
        return value

    def validate(self, attr):
        """其它校验"""
        return attr


class CDAValidateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDAValidateModel
        fields = '__all__'

    def validate(self, attrs):
        """校验cda"""
        match attrs['type']:
            case 'C0001':
                CDAUtils.validate_c0001(data=attrs['file'])
            case _:
                pass

        return attrs

    def create(self, validated_data):
        obj = CDAValidateModel(type=validated_data.get('type'), file=validated_data.get('file').name)
        return obj
