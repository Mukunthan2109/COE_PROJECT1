/**
 * Bilingual UI Toggle (English / Tamil)
 * Provides instant client-side translations for farmer-facing elements.
 */

const translations = {
    en: {
        "nav_home": "Home",
        "nav_observe": "Report Crop Observation",
        "nav_status": "Track Observation",
        "nav_expert": "Expert Dashboard",
        "app_title": "Crop Health Triage & Escalation",
        "app_subtitle": "Farmer-Friendly Crop Disease Triage for Quality Assurance",
        "hero_heading": "Early Crop Disease Observation & Expert Escalation",
        "hero_sub": "Submit crop health photos and visible symptoms for instant screening and rapid expert review.",
        "btn_report": "Report Crop Observation",
        "btn_track": "Track Review Status",
        
        // Form Labels
        "form_title": "Crop Disease Observation Form",
        "lbl_crop": "Select Crop Type",
        "lbl_symptom": "Select Visible Symptom",
        "lbl_stage": "Select Crop Growth Stage",
        "lbl_region": "Select General Region/Zone",
        "lbl_image": "Upload Crop Image",
        "lbl_notes": "Additional Observation Notes (Optional)",
        "btn_submit": "Submit Crop Observation",
        
        // Options - Crops
        "crop_tomato": "Tomato (தக்காளி)",
        "crop_potato": "Potato (உருளைக்கிழங்கு)",
        "crop_chili": "Chili (மிளகாய்)",
        
        // Options - Symptoms
        "sym_spot": "Leaf Spot / Dark Spots",
        "sym_blight": "Blight / Lesions",
        "sym_curl": "Leaf Curl / Crumpled Leaf",
        "sym_healthy": "Healthy (No visible disease)",
        "sym_yellowing": "Yellowing / Discoloration",

        // Results
        "res_header": "Initial Screening Result",
        "res_disclaimer": "This result is an initial screening/triage result, not a definitive expert diagnosis.",
        "res_confidence": "ML Screening Confidence",
        "res_indicators": "Possible Visual Indicators Observed",
        "res_escalated": "This observation has been automatically sent for expert review due to low confidence or unknown category.",
        "res_validated": "Validated by Agricultural Expert",

        // Quality Error
        "qual_error_title": "Image Quality Check Failed",
        "qual_error_msg": "Image quality is insufficient. Please capture a clearer crop image."
    },
    ta: {
        "nav_home": "முகப்பு",
        "nav_observe": "பயிர் நோயைப் பதிவுசெய்க",
        "nav_status": "நிலையைக் கண்காணிக்க",
        "nav_expert": "வல்லுநர் டாஷ்போர்டு",
        "app_title": "பயிர் சுகாதார திரையிடல் மற்றும் பரிந்துரை",
        "app_subtitle": "உணவு பதப்படுத்தும் அலகுகளுக்கான விவசாயி நட்பு பயிர் நோய் கண்டறிதல்",
        "hero_heading": "ஆரம்ப பயிர் நோய் கவனிப்பு மற்றும் வல்லுநர் மதிப்பாய்வு",
        "hero_sub": "உடனடி திரையிடல் மற்றும் விரைவான வல்லுநர் மதிப்பாய்வுக்கு பயிர் சுகாதார படங்கள் மற்றும் அறிகுறிகளைப் சமர்ப்பிக்கவும்.",
        "btn_report": "பயிர் கவனிப்பைப் பதிவுசெய்க",
        "btn_track": "மதிப்பாய்வு நிலையைக் காண்க",

        // Form Labels
        "form_title": "பயிர் நோய் கவனிப்பு படிவம்",
        "lbl_crop": "பயிர் வகையைத் தேர்ந்தெடுக்கவும்",
        "lbl_symptom": "காணக்கூடிய அறிகுறியைத் தேர்ந்தெடுக்கவும்",
        "lbl_stage": "பயிர் வளர்ச்சி நிலையைத் தேர்ந்தெடுக்கவும்",
        "lbl_region": "பொதுவான பிராந்தியம் / மண்டலத்தைத் தேர்ந்தெடுக்கவும்",
        "lbl_image": "பயிர் படத்தைப் பதிவேற்றவும்",
        "lbl_notes": "கூடுதல் கவனிப்பு குறிப்புகள் (விருப்பத்தேர்வு)",
        "btn_submit": "பயிர் கவனிப்பைச் சமர்ப்பிக்கவும்",

        // Options - Crops
        "crop_tomato": "தக்காளி (Tomato)",
        "crop_potato": "உருளைக்கிழங்கு (Potato)",
        "crop_chili": "மிளகாய் (Chili)",

        // Options - Symptoms
        "sym_spot": "இலை புள்ளி / கருமையான புள்ளிகள்",
        "sym_blight": "பயிர்ப் புண் / கருகல் நோய்",
        "sym_curl": "இலை சுருள் / மடிந்த இலை",
        "sym_healthy": "ஆரோக்கியமானது (நோய் அறிகுறிகள் இல்லை)",
        "sym_yellowing": "மஞ்சள் நிறமாதல் / நிறமாற்றம்",

        // Results
        "res_header": "ஆரம்ப திரையிடல் முடிவு",
        "res_disclaimer": "இந்த முடிவு ஒரு ஆரம்ப திரையிடல் முடிவு மட்டுமே, இது இறுதி வல்லுநர் நோயறிதல் அல்ல.",
        "res_confidence": "இயந்திர கற்றல் திரையிடல் நம்பிக்கை நிலை",
        "res_indicators": "கவனிக்கப்பட்ட சாத்தியமான காட்சி குறிகாட்டிகள்",
        "res_escalated": "குறைந்த நம்பிக்கை அல்லது தெரியாத வகை காரணமாக இந்த கவனிப்பு வல்லுநர் மதிப்பாய்வுக்கு தானாகவே அனுப்பப்பட்டுள்ளது.",
        "res_validated": "வேளாண் வல்லுநரால் உறுதிப்படுத்தப்பட்டது",

        // Quality Error
        "qual_error_title": "படத்தின் தரம் போதாது",
        "qual_error_msg": "படத்தின் தரம் போதாது. தயவுசெய்து தெளிவான பயிர் படத்தைப் பிடிக்கவும்."
    }
};

let currentLang = localStorage.getItem('app_lang') || 'en';

function setLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    localStorage.setItem('app_lang', lang);

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });

    // Update active button state
    document.querySelectorAll('.lang-btn').forEach(btn => {
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('btn-success');
            btn.classList.remove('btn-outline-secondary');
        } else {
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-secondary');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLang);

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const selectedLang = e.target.getAttribute('data-lang');
            setLanguage(selectedLang);
        });
    });
});
