/**
 * AgriShield Bilingual UI Toggle (English / Tamil)
 */

const translations = {
    en: {
        "brand_name": "AgriShield",
        "nav_home": "Home",
        "nav_observe": "New Observation",
        "nav_history": "History",
        "nav_expert": "Expert Portal",
        "nav_analytics": "Analytics Dashboard",
        "nav_evaluation": "System Evaluation",
        "nav_feedback": "Feedback",
        
        "hero_heading": "Early Crop Disease Observation & Expert Escalation",
        "hero_sub": "Submit crop health photos and visible symptoms for instant ML screening and rapid agricultural expert verification.",
        "btn_report": "Submit New Observation",
        "btn_expert_dash": "View Expert Dashboard",
        
        "card_total_obs": "Total Recorded Observations",
        "card_escalated": "Escalated to Experts",
        "card_validated": "Expert Validated Cases",
        
        "form_title": "New Observation",
        "form_sub": "Please fill in the crop details and upload a clear photo of the observed symptoms.",
        
        "step1_title": "Step 1: Upload / Capture Crop Image",
        "step1_sub": "Select a clear photo of the affected plant foliage, stem, or fruit from your gallery or mobile camera. (Max 5 MB, JPG/PNG)",
        "step1_drag": "Click or tap above to select / capture a crop photo",

        "step2_title": "Step 2: Select Crop Type",
        "step3_title": "Step 3: Select Growth Stage",
        "step4_title": "Step 4: Select Visible Symptoms",
        "step5_title": "Step 5: Select Location / Region",

        "btn_submit": "Submit Observation for Screening"
    },
    ta: {
        "brand_name": "அக்ரிஷீல்ட் (AgriShield)",
        "nav_home": "முகப்பு",
        "nav_observe": "புதிய கவனிப்பு",
        "nav_history": "வரலாறு",
        "nav_expert": "வல்லுநர் போர்ட்டல்",
        "nav_analytics": "பகுப்பாய்வு டாஷ்போர்டு",
        "nav_evaluation": "அமைப்பின் மதிப்பீடு",
        "nav_feedback": "கருத்துக்கள்",

        "hero_heading": "ஆரம்ப பயிர் நோய் கவனிப்பு மற்றும் வல்லுநர் பரிந்துரை",
        "hero_sub": "உடனடி கணினி திரையிடல் மற்றும் விரைவான வேளாண் வல்லுநர் சரிபார்ப்புக்கு பயிர் சுகாதார படங்கள் மற்றும் அறிகுறிகளை சமர்ப்பிக்கவும்.",
        "btn_report": "புதிய கவனிப்பை சமர்ப்பிக்கவும்",
        "btn_expert_dash": "வல்லுநர் டாஷ்போர்டைக் காண்க",

        "card_total_obs": "பதிவு செய்யப்பட்ட மொத்த கவனிப்புகள்",
        "card_escalated": "வல்லுநர்களுக்கு பரிந்துரைக்கப்பட்டவை",
        "card_validated": "வல்லுநரால் உறுதிப்படுத்தப்பட்டவை",

        "form_title": "புதிய கவனிப்பு",
        "form_sub": "பயிர் விவரங்களை பூர்த்தி செய்து, கவனிக்கப்பட்ட அறிகுறிகளின் தெளிவான புகைப்படத்தை பதிவேற்றவும்.",

        "step1_title": "படி 1: பயிர் படத்தைப் பதிவேற்றவும் / பிடிக்கவும்",
        "step1_sub": "பாதிக்கப்பட்ட தாவர இலை அல்லது பழத்தின் தெளிவான புகைப்படத்தை தேர்ந்தெடுக்கவும்.",
        "step1_drag": "பயிர் புகைப்படத்தை தேர்ந்தெடுக்க இங்கே கிளிக் செய்யவும்",

        "step2_title": "படி 2: பயிர் வகையைத் தேர்ந்தெடுக்கவும்",
        "step3_title": "படி 3: வளர்ச்சி நிலையைத் தேர்ந்தெடுக்கவும்",
        "step4_title": "படி 4: காணப்படும் அறிகுறிகளைத் தேர்ந்தெடுக்கவும்",
        "step5_title": "படி 5: பிராந்தியத்தைத் தேர்ந்தெடுக்கவும்",

        "btn_submit": "திரையிடலுக்கு கவனிப்பைச் சமர்ப்பிக்கவும்"
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

    const langBtn = document.getElementById('langToggleBtn');
    if (langBtn) {
        langBtn.textContent = lang === 'en' ? 'தமிழ்' : 'English';
    }
}

function toggleLanguage() {
    const nextLang = currentLang === 'en' ? 'ta' : 'en';
    setLanguage(nextLang);
}

document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLang);
    const langBtn = document.getElementById('langToggleBtn');
    if (langBtn) {
        langBtn.addEventListener('click', toggleLanguage);
    }
});
