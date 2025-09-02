# FarmManager/constants.py
"""
Constants and message templates for the Farm Manager application
"""

# Message Types
class MessageTypes:
    HEAT_ALERT = "heat_alert"
    HEALTH_ALERT = "health_alert" 
    VACCINATION_ALERT = "vaccination_alert"
    PREGNANCY_UPDATE = "pregnancy_update"
    INSEMINATION_ALERT = "insemination_alert"
    FARMER_ALERT = "farmer_alert"
    DOCTOR_ALERT = "doctor_alert"
    DOCTOR_ASSIGNMENT = "doctor_assignment"
    INSEMINATOR_ASSIGNMENT = "inseminator_assignment"
    PREGNANCY_CONFIRMATION = "pregnancy_confirmation"
    BIRTH_ALERT = "birth_alert"
    CALVING_2_MONTHS_ALERT = "calving_2_months_alert"
    CALVING_1_MONTH_ALERT = "calving_1_month_alert"
    CALVING_DUE_ALERT = "calving_due_alert"
    HEAT_MONITORING_ALERT = "heat_monitoring_alert"
    DOCTOR_CONFIRMATION = "doctor_confirmation"
    OTHER = "other"


# Default Health Status Names
class DefaultHealthStatus:
    GENERAL_HEALTH_NORMAL = "normal"
    UDDER_HEALTH_NORMAL = "4qt_normal"
    MASTITIS_CLINICAL = "negative"


# Message Templates in Amharic
class MessageTemplates:
    @staticmethod
    def insemination_alert(farm_id, owner_name, address, phone, cow_id, heat_signs):
        return (
            f"የማዳቀያ ማንቂያ\n"
            f"እርባታ ጣቢያ ({farm_id}) - {owner_name}\n"
            f"አድራሻ: {address}\n"
            f"ስልክ ቁ: {phone}\n"
            f"የላም መለያ ቁጥር: {cow_id}\n"
            f"የኮርማ ፍላጎት ምልክቶች: {heat_signs}\n"
            f"እባክዎን ከቀኑ (4 ሰዓት) እሰከ (7 ሰዓት) ባለው ጊዜ ያዳቅሉ::"
        )
    
    @staticmethod
    def farmer_heat_notification(cow_id, inseminator_name):
        return (
            f"ማንቂያ፡- የላምዎ መለያ ቁጥር ({cow_id}) የፍላጎት ምልክቶችን ስለሚያሳይ የእርስዎ ማዳቀያ ({inseminator_name}) ማሳወቂያ ደርሶታል። በቅርቡ እርሻዎን ይጎበኛሉ።"
        )
    
    @staticmethod
    def pregnancy_confirmation(cow_id, pregnancy_date, expected_calving_date, lactation_number):
        return (
            f"🐄 እርግዝና ተመዝግቧል!\n"
            f"ላም፦ {cow_id}\n"
            f"የእርግዝና ቀን፡ {pregnancy_date}\n"
            f"የሚጠበቀው የመውለጃ ቀን፡ {expected_calving_date}\n"
            f"የመወለድ ቁጥር፡ {lactation_number}"
        )
    
    @staticmethod
    def farmer_medical_report_confirmation(cow_id, sickness_description, doctor_name):
        return (
            f"✅ የህክምና ሪፖርት ደርሷል\n"
            f"ላም፦ {cow_id}\n"
            f"ጉዳይ ሪፖርት ተደርጓል፡ {sickness_description}\n"
            f"ሪፖርትህ ለዶክተር {doctor_name} ተልኳል።\n"
            f"ከግምገማው በኋላ ማሳወቂያ ይደርስዎታል።"
        )
    
    @staticmethod
    def doctor_medical_report_alert(cow_id, farm_id, owner_name, sickness_description):
        return (
            f"አዲስ የወተት አርቢ የእንስሳት ጤና ሪፖርት\n"
            f"ላም: {cow_id}\n"
            f"የእርባታ ጣቢያ: {farm_id}\n"
            f"የሐኪሙ ስም: {owner_name}\n"
            f"ሪፖርት የሚደረገው ጉዳይ: {sickness_description}\n"
            f"አባክዎን በሪፖርቱ የተጠቀሰውን ይከታተሉ"
        )
    
    @staticmethod
    def medical_assessment_complete(cow_id, doctor_name, is_sick, has_lameness, notes):
        sickness_status = "ታማሚ" if is_sick else "ጤናማ"
        lameness_status = "አዎ" if has_lameness else "አይደለም"
        return (
            f"የሕክምና ግምገማ ተጠናቋል\n"
            f"ላም፦ {cow_id}\n"
            f"ዶክተር፡ ዶክተር {doctor_name}\n"
            f"የጤና ሁኔታ፡ {sickness_status}\n"
            f"አንካሳ፡ {lameness_status}\n"
            f"ማስታወሻዎች፡ {notes or 'N/A'}"
        )
    
    @staticmethod
    def doctor_assessment_confirmation(farm_id, owner_name, cow_id, is_sick):
        sickness_status = "ታማሚ" if is_sick else "ጤናማ"
        return (
            f"✅ ግምገማ ተመዝግቧል\n"
            f"እርሻ፡ {farm_id} - {owner_name}\n"
            f"ላም፦ {cow_id}\n"
            f"ሁኔታ፡ {sickness_status}\n"
            f"የግምገማ ውጤቱን አርሶ አደሩ እንዲያውቅ ተደርጓል።"
        )
    
    @staticmethod
    def heat_monitoring_farmer(cow_id, farm_id, owner_name, is_inseminated, insemination_count, insemination_date=None):
        status = "ተዳቅላለች" if is_inseminated else "አልተዳቀለችም"
        message = (
            f"የኮርማ ፍላጎት መከታተያ\n"
            f"ላም: {cow_id}\n"
            f"የእርባታ ጣቢያ: {farm_id} {owner_name}\n"
            f"ሁኔታ: {status}\n"
            f"የድቀላ ብዛት: {insemination_count}"
        )
        if is_inseminated and insemination_date:
            message += f"\nየተዳቀለችበት ቀን: {insemination_date}"
        return message
    
    @staticmethod
    def heat_monitoring_inseminator(farm_id, cow_id, is_inseminated, lactation_number, insemination_count, insemination_date=None):
        status = "ተዳቅላለች" if is_inseminated else "አልተዳቀለችም"
        message = (
            f"✅ ሪከርድ ደረሰ\n"
            f"እርሻ፡ {farm_id}\n"
            f"ላም፦ {cow_id}\n"
            f"ሁኔታ፡ {status}\n"
            f"የጡት ማጥባት ቁጥር፡ {lactation_number}\n"
            f"የማዳቀል ብዛት፡ {insemination_count}"
        )
        if is_inseminated and insemination_date:
            message += f"\nየተዳቀለችበት ቀን፡ {insemination_date}"
        return message
    
    @staticmethod
    def birth_event(cow_id, calving_date, last_calving_date, calf_sex):
        calf_sex_amharic = "ወንድ" if calf_sex == "M" else "ሴት"
        return (
            f"🎉 የልደት ክስተት ተመዝግቧል!\n"
            f"ላም፦ {cow_id}\n"
            f"የትውልድ ቀን፡ {calving_date}\n"
            f"የመጨረሻው የመውለጃ ቀን፡ {last_calving_date}\n"
            f"የጥጃ ጾታ፡ {calf_sex_amharic}"
        )
    
    @staticmethod
    def staff_assignment_notice(staff_type, farm_id, owner_name, address, phone):
        return (
            f"Notice: You have been assigned to a new farm:\n"
            f"Farm ID: {farm_id}\n"
            f"Owner: {owner_name}\n"
            f"Address: {address}\n"
            f"Phone: {phone}"
        )
    
    @staticmethod
    def staff_unassignment_notice(farm_id, owner_name):
        return (
            f"Notice: You have been unassigned from farm: {farm_id} "
            f"({owner_name})"
        )
    
    @staticmethod
    def doctor_change_farmer_notice(doctor_name, doctor_phone):
        return (
            f"Notice: Your farm's doctor has been changed to Dr.{doctor_name}. "
            f"Contact number: {doctor_phone}"
        )
    
    @staticmethod
    def calving_2_months_alert(cow_id, expected_calving_date, lactation_number):
        return (
            f"🐄 የመውለጃ ማስታወሻ - 2 ወር ቀርቷል\n"
            f"ላም፦ {cow_id}\n"
            f"የሚጠበቀው የመውለጃ ቀን፡ {expected_calving_date}\n"
            f"የመወለድ ቁጥር፡ {lactation_number}\n"
            f"እባክዎን ላሙን ለመውለጃ ማዘጋጀት ይጀምሩ"
        )
    
    @staticmethod
    def calving_1_month_alert(cow_id, expected_calving_date, lactation_number):
        return (
            f"🚨 የመውለጃ ማስታወሻ - 1 ወር ቀርቷል\n"
            f"ላም፦ {cow_id}\n"
            f"የሚጠበቀው የመውለጃ ቀን፡ {expected_calving_date}\n"
            f"የመወለድ ቁጥር፡ {lactation_number}\n"
            f"እባክዎን ላሙን በቅርብ ይከታተሉ እና ለመውለጃ ዝግጅት ያድርጉ"
        )
    
    @staticmethod
    def calving_due_alert(cow_id, expected_calving_date, lactation_number):
        return (
            f"⚠️ የመውለጃ ቀን ደርሷል!\n"
            f"ላም፦ {cow_id}\n"
            f"የሚጠበቀው የመውለጃ ቀን፡ {expected_calving_date}\n"
            f"የመወለድ ቁጥር፡ {lactation_number}\n"
            f"እባክዎን ላሙን በትኩረት ይከታተሉ እና አስፈላጊውን እርዳታ ይስጡ"
        )
    
    @staticmethod
    def heat_monitoring_reminder(cow_id, days_since_heat, last_heat_date):
        return (
            f"🔄 የኮርማ ፍላጎት ማስታወሻ\n"
            f"ላም፦ {cow_id}\n"
            f"ከመጨረሻው የኮርማ ምልክት ጀምሮ፡ {days_since_heat} ቀናት\n"
            f"የመጨረሻው የኮርማ ቀን፡ {last_heat_date}\n"
            f"እባክዎን ላሙን የኮርማ ምልክቶች ይከታተሉ"
        )


# API Response Messages
class APIMessages:
    HEAT_SIGN_RECORDED = "Heat sign recorded and alert sent successfully"
    PREGNANCY_UPDATED = "Pregnancy monitoring record updated successfully"
    MEDICAL_ASSESSMENT_SUBMITTED = "Medical assessment submitted successfully"
    MEDICAL_ASSESSMENT_RECORDED = "Medical assessment recorded successfully"
    HEAT_SIGN_MONITORING_RECORDED = "Heat sign monitoring recorded successfully"
    BIRTH_EVENT_RECORDED = "Birth event recorded successfully"
    STAFF_CHANGED_SUCCESSFULLY = "Staff changed successfully"
    
    # Error messages
    FARM_ID_REQUIRED = "farm_id query parameter is required"
    FAILED_TO_CREATE_FARM = "Failed to create farm"
    FAILED_TO_UPDATE_FARM = "Failed to update farm"
    FAILED_TO_RETRIEVE_FARM = "Failed to retrieve farm"
    FAILED_TO_DELETE_FARM = "Failed to delete farm"
    FAILED_TO_UPDATE_PREGNANCY = "Failed to update pregnancy status"
    FAILED_TO_SUBMIT_MEDICAL_ASSESSMENT = "Failed to submit medical assessment"
    FAILED_TO_RECORD_MEDICAL_ASSESSMENT = "Failed to record medical assessment"
    FAILED_TO_RECORD_HEAT_MONITORING = "Failed to record heat sign monitoring"
    FAILED_TO_RECORD_BIRTH = "Failed to record birth event" 