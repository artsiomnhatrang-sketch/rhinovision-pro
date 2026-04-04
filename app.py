import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw
import io
import base64
import json
import re
import urllib.request

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RhinoVision Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
}
[data-testid="stAppViewContainer"] > .main { background: #f0f4f8; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2rem 2rem !important; max-width: 1440px !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Header ── */
.rv-header {
    background: #1a2b4a;
    padding: 0 2rem;
    margin: 0 -2rem 0 -2rem;
    height: 64px;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.rv-logo {
    width: 38px; height: 38px;
    background: #0066cc;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem; font-weight: 900; color: white;
    letter-spacing: -1px; flex-shrink: 0;
}
.rv-brand { display: flex; flex-direction: column; }
.rv-name {
    font-size: 1.15rem; font-weight: 800;
    color: #ffffff; letter-spacing: -0.3px; line-height: 1.1;
}
.rv-name span { color: #60a5fa; }
.rv-tagline { font-size: 0.72rem; color: #94a3b8; margin-top: 1px; }
.rv-ai-badge {
    font-size: 0.65rem; color: #34d399;
    background: rgba(52,211,153,0.15); padding: 3px 10px;
    border-radius: 20px; border: 1px solid rgba(52,211,153,0.3);
}
.rv-version {
    margin-left: auto;
    font-size: 0.65rem; color: #64748b;
    background: #243350; padding: 3px 10px; border-radius: 20px;
}

/* ── Cards ── */
.rv-card-title {
    font-size: 0.65rem; font-weight: 700;
    color: #1a2b4a; text-transform: uppercase;
    letter-spacing: 1.3px; margin-bottom: 0.9rem;
    padding-bottom: 0.5rem; border-bottom: 2px solid #e8edf2;
    display: flex; align-items: center; gap: 0.4rem;
}
.rv-card-title::before {
    content: "";
    display: block; width: 3px; height: 13px;
    background: #0066cc; border-radius: 2px;
}

/* ── API key status ── */
.rv-status {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.75rem; padding: 4px 12px;
    border-radius: 20px; margin-bottom: 0.5rem; margin-top: 0.25rem;
}
.rv-status-ready { background: rgba(52,211,153,0.1); color: #059669; border: 1px solid rgba(52,211,153,0.3); }
.rv-status-nokey { background: rgba(245,158,11,0.1); color: #b45309; border: 1px solid rgba(245,158,11,0.3); }

/* ── Analysis grid ── */
.rv-analysis-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 0.5rem; }
.rv-analysis-card {
    background: #f8fafc; border: 1px solid #e8edf2;
    border-radius: 8px; padding: 0.75rem 1rem;
}
.rv-analysis-card h4 {
    font-size: 0.63rem; font-weight: 700; color: #64748b;
    text-transform: uppercase; letter-spacing: 1px; margin: 0 0 0.5rem 0;
}
.rv-metric { display: flex; justify-content: space-between; font-size: 0.78rem; padding: 3px 0; border-bottom: 1px solid #f1f5f9; }
.rv-metric:last-child { border-bottom: none; }
.rv-metric-key { color: #64748b; }
.rv-metric-val { color: #1a2b4a; font-weight: 600; }
.rv-surgical-note {
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;
    padding: 0.75rem 1rem; margin-top: 0.75rem; font-size: 0.82rem;
    color: #1e40af; grid-column: 1 / -1; line-height: 1.5;
}

/* ── Empty state ── */
.rv-empty {
    background: #f8fafc; border: 2px dashed #cbd5e1;
    border-radius: 12px; padding: 3rem 2rem; text-align: center;
    color: #64748b; margin-top: 0.5rem;
}
.rv-empty-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
.rv-empty-text { font-size: 0.82rem; line-height: 1.6; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    transition: all 0.15s ease !important;
}
[data-testid="stBaseButton-primary"] { background: #0066cc !important; border: none !important; }
[data-testid="stBaseButton-primary"]:hover {
    background: #0052a3 !important;
    box-shadow: 0 4px 14px rgba(0,102,204,0.35) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stDownloadButton"] > button {
    background: #16a34a !important; color: white !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input {
    border-radius: 8px !important; border-color: #cbd5e1 !important; font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #0066cc !important; box-shadow: 0 0 0 3px rgba(0,102,204,0.15) !important;
}
[data-testid="stFileUploader"] {
    border: 2px dashed #bfdbfe !important; border-radius: 10px !important; background: #eff6ff !important;
}
[data-testid="stSlider"] [role="slider"] { background: #0066cc !important; border-color: #0066cc !important; }

/* ── Disclaimer ── */
.rv-disclaimer {
    font-size: 0.66rem; color: #94a3b8; line-height: 1.7;
    text-align: center; padding: 1rem 3rem;
    background: #f8fafc; border-radius: 10px;
    border-top: 2px solid #e8edf2; margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rv-header">
  <div class="rv-logo">RV</div>
  <div class="rv-brand">
    <div class="rv-name">RhinoVision <span>Pro</span></div>
    <div class="rv-tagline">Профессиональный симулятор ринопластики для пластических хирургов</div>
  </div>
  <div class="rv-ai-badge">⚡ Gemini AI Pipeline</div>
  <div class="rv-version">v3.1 · FLUX</div>
</div>
""", unsafe_allow_html=True)

# ─── Session state ─────────────────────────────────────────────────────────────
_DEFAULTS = {
    "orig": None, "orig_bytes": None, "result": None,
    "analysis": None, "rc": 0, "last_name": "",
    "patient_name": "", "annotations": [],
    "gemini_key": "", "replicate_token": "",
    "gen_error": None, "analysis_error": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Image helpers ─────────────────────────────────────────────────────────────

def load_pil(f):
    try:
        return Image.open(f).convert("RGB")
    except Exception as e:
        st.error(f"Ошибка загрузки: {e}")
        st.stop()

def fit(img, mx=768):
    w, h = img.size
    if max(w, h) <= mx:
        return img
    r = mx / max(w, h)
    return img.resize((int(w * r), int(h * r)), Image.LANCZOS)

def pil_to_bytes(img, quality=92):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()

def pil_to_b64(img):
    return base64.b64encode(pil_to_bytes(img)).decode()

def apply_annotations(base_img, annotations):
    if not annotations:
        return base_img
    out = base_img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for ann in annotations:
        color = ann.get("color", "#FF3333")
        thick = ann.get("thick", 3)
        kind  = ann.get("kind", "circle")
        cx, cy = int(w * ann["rx"]), int(h * ann["ry"])
        r = int(min(w, h) * 0.07)
        if kind == "circle":
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=thick)
        elif kind == "arrow":
            draw.line([cx-r, cy, cx+r, cy], fill=color, width=thick)
            draw.polygon([cx+r, cy-6, cx+r, cy+6, cx+r+12, cy], fill=color)
        elif kind == "line":
            draw.line([cx-r, cy, cx+r, cy], fill=color, width=thick)
    return out

def comparison_slider(before_img, after_img, height=420):
    b64b = pil_to_b64(before_img)
    b64a = pil_to_b64(after_img)
    html = f"""
<style>
.cmp-wrap {{
  position:relative;width:100%;max-width:780px;height:{height}px;
  overflow:hidden;border-radius:12px;border:1px solid #e8edf2;
  user-select:none;cursor:col-resize;box-shadow:0 4px 16px rgba(0,0,0,.10);
}}
.cmp-wrap img {{
  position:absolute;top:0;left:0;width:100%;height:100%;
  object-fit:cover;pointer-events:none;display:block;
}}
.cmp-after {{ clip-path:inset(0 0 0 50%); }}
.cmp-divider {{
  position:absolute;top:0;left:50%;width:2px;height:100%;
  background:#fff;box-shadow:0 0 6px rgba(0,0,0,.4);pointer-events:none;
}}
.cmp-handle {{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:44px;height:44px;border-radius:50%;background:#fff;
  box-shadow:0 2px 10px rgba(0,0,0,.3);display:flex;align-items:center;
  justify-content:center;font-size:1.1rem;pointer-events:none;
}}
.cmp-label {{
  position:absolute;top:12px;font-size:.65rem;font-weight:700;
  letter-spacing:1px;text-transform:uppercase;padding:3px 10px;
  border-radius:20px;pointer-events:none;
}}
.cmp-label-before {{ left:12px;background:rgba(0,0,0,.45);color:#e5e7eb; }}
.cmp-label-after  {{ right:12px;background:rgba(0,102,204,.75);color:#fff; }}
</style>
<div class="cmp-wrap" id="cmp">
  <img class="cmp-before" src="data:image/jpeg;base64,{b64b}"/>
  <img class="cmp-after"  src="data:image/jpeg;base64,{b64a}" id="cmpAfter"/>
  <div class="cmp-divider" id="cmpDiv"></div>
  <div class="cmp-handle"  id="cmpHandle">&#8660;</div>
  <div class="cmp-label cmp-label-before">ДО</div>
  <div class="cmp-label cmp-label-after">ПОСЛЕ</div>
</div>
<script>
(function(){{
  var wrap=document.getElementById('cmp'),
      after=document.getElementById('cmpAfter'),
      div=document.getElementById('cmpDiv'),
      handle=document.getElementById('cmpHandle'),
      drag=false;
  function setPos(p){{
    p=Math.min(Math.max(p,2),98);
    after.style.clipPath='inset(0 0 0 '+p+'%)';
    div.style.left=p+'%';handle.style.left=p+'%';
  }}
  wrap.addEventListener('mousedown',function(){{drag=true;}});
  wrap.addEventListener('touchstart',function(){{drag=true;}},{{passive:true}});
  document.addEventListener('mouseup',function(){{drag=false;}});
  document.addEventListener('touchend',function(){{drag=false;}});
  document.addEventListener('mousemove',function(e){{
    if(!drag)return;
    var r=wrap.getBoundingClientRect();
    setPos((e.clientX-r.left)/r.width*100);
  }});
  document.addEventListener('touchmove',function(e){{
    if(!drag)return;
    var r=wrap.getBoundingClientRect();
    setPos((e.touches[0].clientX-r.left)/r.width*100);
  }},{{passive:true}});
}})();
</script>
"""
    components.html(html, height=height + 10, scrolling=False)

# ─── AI helpers ───────────────────────────────────────────────────────────────

_ANALYSIS_PROMPT = """Analyze this facial photo for rhinoplasty surgical planning.
Return ONLY a valid JSON object — no markdown, no extra text — with this exact structure:
{
  "nose": {
    "bridge_width": "narrow|medium|wide",
    "dorsal_hump": "absent|mild|moderate|severe",
    "tip_projection": "deprojected|average|projected",
    "nostril_width": "narrow|medium|wide",
    "nose_length": "short|average|long",
    "tip_rotation": "downward|neutral|upward",
    "skin_thickness": "thin|medium|thick",
    "tip_definition": "refined|average|bulbous",
    "symmetry": "symmetric|mild asymmetry|asymmetric"
  },
  "face": {
    "face_shape": "oval|round|square|heart|diamond",
    "skin_tone": "fair|light|medium|olive|tan|dark",
    "complexion": "clear|mild texture|combination",
    "estimated_age": "18-25|25-35|35-45|45+"
  },
  "photo": {
    "lighting_quality": "excellent|good|fair|poor",
    "lighting_direction": "frontal|lateral|overhead|mixed",
    "shadows": "minimal|moderate|harsh",
    "background": "neutral/clinical|complex",
    "framing": "optimal|suboptimal"
  },
  "surgical_notes": "One professional sentence on key rhinoplasty considerations for this patient."
}"""


def _pct(value, max_val):
    return int(abs(value) / max_val * 100)

def _intensity(pct):
    if pct < 25: return "slightly"
    if pct < 55: return "moderately"
    return "significantly"

def build_flux_prompt(params, analysis=None):
    """Build img2img prompt for FLUX Schnell rhinoplasty simulation."""
    changes = []
    specs = [
        ("hump",          50, "reduced dorsal nasal hump",      "heightened nasal bridge"),
        ("tip_proj",      50, "deprojected nasal tip",          "more projected nasal tip"),
        ("nose_width",    50, "narrower nasal bridge",          "wider nasal bridge"),
        ("nostril_width", 50, "smaller nostrils",               "larger nostrils"),
        ("tip_angle",     30, "downward-rotated nasal tip",     "upward-rotated nasal tip"),
        ("nose_length",   50, "shorter nose",                   "elongated nose"),
    ]
    for key, mx, down_desc, up_desc in specs:
        v = params[key]
        if abs(v) <= 3:
            continue
        p = _pct(v, mx)
        desc = down_desc if v < 0 else up_desc
        changes.append(f"{_intensity(p)} {desc}")

    # Incorporate Gemini analysis for more accurate face description
    face_desc = ""
    if analysis:
        face = analysis.get("face", {})
        parts = []
        if face.get("skin_tone"):    parts.append(f"{face['skin_tone']} skin tone")
        if face.get("face_shape"):   parts.append(f"{face['face_shape']} face shape")
        if face.get("estimated_age"): parts.append(f"{face['estimated_age']} years old")
        if parts:
            face_desc = ", ".join(parts) + ", "

    nose_desc = ", ".join(changes) if changes else "unchanged natural nose"
    return (
        f"Photorealistic medical portrait, {face_desc}same person, "
        f"post-rhinoplasty simulation with {nose_desc}. "
        f"Professional clinical photograph, identical lighting and background, "
        f"natural skin texture, highly detailed, photographic quality."
    )


def _read_replicate_output(output):
    """Robustly extract raw image bytes from any Replicate output shape."""
    # Materialise iterators/generators without consuming twice
    if hasattr(output, '__iter__') and not isinstance(output, (str, bytes)):
        items = list(output)
    else:
        items = [output]

    for item in items:
        if item is None:
            continue
        # FileOutput.read() — newest SDK
        if hasattr(item, 'read'):
            data = item.read()
            if data:
                return bytes(data)
        # FileOutput.url or plain URL string
        url = None
        if hasattr(item, 'url'):
            url = str(item.url)
        elif isinstance(item, str) and item.startswith("http"):
            url = item
        if url:
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    return r.read()
            except Exception:
                continue
        # Raw bytes
        if isinstance(item, (bytes, bytearray)):
            return bytes(item)
    return None


def _classify_replicate_error(err_str):
    e = err_str.lower()
    if "401" in e or "invalid token" in e or "unauthorized" in e or "authentication" in e:
        return "Неверный Replicate токен. Проверьте токен на replicate.com/account/api-tokens"
    if "402" in e or "payment" in e or "billing" in e:
        return "Требуется оплата Replicate. Пополните баланс на replicate.com/account/billing"
    if "429" in e or "rate limit" in e or "too many" in e:
        return "Превышен лимит запросов Replicate. Подождите немного и повторите."
    if "nsfw" in e or "safety" in e or "content" in e:
        return "Контент заблокирован фильтром безопасности. Используйте другое фото."
    if "timeout" in e or "timed out" in e:
        return "Таймаут Replicate. Попробуйте снова."
    if "model" in e and ("not found" in e or "doesn't exist" in e):
        return "Модель FLUX не найдена. Проверьте подключение."
    return f"Ошибка Replicate: {err_str[:200]}"


def generate_with_replicate(rep_token, img_bytes, params, analysis=None):
    """Phase 2 — text-to-image with Replicate FLUX Schnell."""
    try:
        import replicate as rep_lib

        client = rep_lib.Client(api_token=rep_token)
        prompt = build_flux_prompt(params, analysis)

        output = client.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "num_outputs": 1,
                "num_inference_steps": 4,
                "output_format": "jpg",
                "output_quality": 90,
                "go_fast": True,
            },
        )

        data = _read_replicate_output(output)
        if not data:
            return None, "Replicate не вернул изображение. Попробуйте снова."
        return Image.open(io.BytesIO(data)).convert("RGB"), None

    except Exception as e:
        return None, _classify_replicate_error(str(e))


def _parse_json_response(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _classify_error(err_str):
    e = err_str.lower()
    if "api_key_invalid" in e or "invalid" in e and "key" in e:
        return "Неверный Gemini API ключ. Проверьте ключ на aistudio.google.com"
    if "quota" in e or "429" in e or "resource_exhausted" in e:
        return "Превышен лимит Gemini API. Подождите минуту и повторите."
    if "safety" in e or "block" in e:
        return "Запрос заблокирован фильтром безопасности Gemini. Попробуйте другое фото."
    if "model" in e and ("not found" in e or "unavailable" in e):
        return "Модель Gemini недоступна в вашем регионе. Попробуйте позже."
    return f"Ошибка Gemini API: {err_str}"


def analyze_face(api_key, img_bytes):
    """Phase 1 — vision analysis with gemini-2.0-flash."""
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                _ANALYSIS_PROMPT,
            ],
        )
        return _parse_json_response(response.text), None
    except json.JSONDecodeError:
        return None, "Gemini вернул неверный JSON. Повторите запрос."
    except Exception as e:
        return None, _classify_error(str(e))


def render_analysis(analysis):
    if not analysis:
        return
    nose = analysis.get("nose", {})
    face = analysis.get("face", {})
    photo = analysis.get("photo", {})
    notes = analysis.get("surgical_notes", "")

    def m(k, v):
        return f'<div class="rv-metric"><span class="rv-metric-key">{k}</span><span class="rv-metric-val">{v or "—"}</span></div>'

    nose_html = (
        m("Ширина спинки",  nose.get("bridge_width"))
        + m("Горбинка",     nose.get("dorsal_hump"))
        + m("Проекция кончика", nose.get("tip_projection"))
        + m("Ширина ноздрей",   nose.get("nostril_width"))
        + m("Длина носа",       nose.get("nose_length"))
        + m("Ротация кончика",  nose.get("tip_rotation"))
        + m("Толщина кожи",     nose.get("skin_thickness"))
        + m("Определение кончика", nose.get("tip_definition"))
        + m("Симметрия",        nose.get("symmetry"))
    )
    face_html = (
        m("Форма лица",   face.get("face_shape"))
        + m("Тон кожи",   face.get("skin_tone"))
        + m("Кожа",       face.get("complexion"))
        + m("Возраст",    face.get("estimated_age"))
        + m("Освещение",  photo.get("lighting_quality"))
        + m("Тени",       photo.get("shadows"))
        + m("Кадр",       photo.get("framing"))
    )
    note_html = (
        f'<div class="rv-surgical-note"><strong>Хирургические заметки:</strong> {notes}</div>'
        if notes else ""
    )
    st.markdown(f"""
<div class="rv-analysis-grid">
  <div class="rv-analysis-card"><h4>Параметры носа</h4>{nose_html}</div>
  <div class="rv-analysis-card"><h4>Лицо и фото</h4>{face_html}</div>
  {note_html}
</div>""", unsafe_allow_html=True)


# ─── Patient info bar ──────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
pi1, pi2, pi3 = st.columns([4, 3, 3])
with pi1:
    pname = st.text_input("👤 Имя пациента",
                          value=st.session_state.patient_name,
                          placeholder="Введите имя пациента...",
                          key=f"pname_{st.session_state.rc}")
    st.session_state.patient_name = pname
with pi2:
    st.text_input("📅 Дата консультации", placeholder="дд.мм.гггг",
                  key=f"pdate_{st.session_state.rc}")
with pi3:
    st.text_input("🏥 Врач", placeholder="ФИО хирурга",
                  key=f"pdoc_{st.session_state.rc}")

st.divider()

# ─── Main layout ───────────────────────────────────────────────────────────────
col_l, col_r = st.columns([4, 6], gap="large")

# ══════════ LEFT — photo ══════════
with col_l:
    st.markdown('<div class="rv-card-title">📸 Фото пациента</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Загрузить фото (JPG · PNG)",
                                type=["jpg", "jpeg", "png"],
                                key=f"up_{st.session_state.rc}")

    if uploaded and uploaded.name != st.session_state.last_name:
        img = fit(load_pil(uploaded))
        st.session_state.orig         = img
        st.session_state.orig_bytes   = pil_to_bytes(img, quality=95)
        st.session_state.result       = None
        st.session_state.analysis     = None
        st.session_state.annotations  = []
        st.session_state.last_name    = uploaded.name
        st.session_state.gen_error    = None
        st.session_state.analysis_error = None

    if st.session_state.orig is None:
        st.markdown("""
<div class="rv-empty">
  <div class="rv-empty-icon">📷</div>
  <div class="rv-empty-text">
    Загрузите фото пациента<br>
    <span style="color:#94a3b8;font-size:0.75rem">JPG · PNG · фронтальный вид</span>
  </div>
</div>""", unsafe_allow_html=True)
    else:
        st.image(apply_annotations(st.session_state.orig, st.session_state.annotations),
                 width=400)

        st.markdown('<div class="rv-card-title" style="margin-top:0.75rem">🖊 Инструменты разметки</div>',
                    unsafe_allow_html=True)
        tc1, tc2, tc3 = st.columns([3, 2, 2])
        with tc1:
            ann_kind = st.radio("Фигура", ["○ Круг", "╱ Линия", "→ Стрелка"],
                                horizontal=False, label_visibility="collapsed",
                                key=f"ann_kind_{st.session_state.rc}")
        with tc2:
            ann_color = st.color_picker("Цвет", "#FF3333",
                                        key=f"ann_color_{st.session_state.rc}")
            ann_thick = st.select_slider("Толщина", [1,2,3,5,8], value=3,
                                         key=f"ann_thick_{st.session_state.rc}")
        with tc3:
            ann_x = st.slider("X %", 10, 90, 50, key=f"ann_x_{st.session_state.rc}")
            ann_y = st.slider("Y %", 10, 90, 43, key=f"ann_y_{st.session_state.rc}")

        kind_map = {"○ Круг": "circle", "╱ Линия": "line", "→ Стрелка": "arrow"}
        ab1, ab2 = st.columns(2)
        with ab1:
            if st.button("➕ Добавить", use_container_width=True, key="btn_add_ann"):
                st.session_state.annotations.append({
                    "kind": kind_map[ann_kind], "color": ann_color,
                    "thick": ann_thick, "rx": ann_x/100, "ry": ann_y/100,
                })
                st.rerun()
        with ab2:
            if st.button("🗑 Очистить", use_container_width=True, key="btn_clr_ann"):
                st.session_state.annotations = []
                st.rerun()

# ══════════ RIGHT — controls ══════════
with col_r:
    # ── API keys ──
    st.markdown('<div class="rv-card-title">🔑 API Ключи</div>', unsafe_allow_html=True)
    key_col1, key_col2 = st.columns(2)
    with key_col1:
        gemini_input = st.text_input(
            "Gemini API Key (анализ лица)",
            type="password",
            value=st.session_state.gemini_key,
            placeholder="AIza...",
            help="Бесплатно на aistudio.google.com → Get API Key",
            key=f"apikey_{st.session_state.rc}",
        )
        st.session_state.gemini_key = gemini_input
    with key_col2:
        rep_input = st.text_input(
            "Replicate Token (генерация FLUX)",
            type="password",
            value=st.session_state.replicate_token,
            placeholder="r8_...",
            help="Получите на replicate.com/account/api-tokens",
            key=f"reptoken_{st.session_state.rc}",
        )
        st.session_state.replicate_token = rep_input

    _both = gemini_input and rep_input
    if _both:
        st.markdown('<div class="rv-status rv-status-ready">⚡ Оба ключа введены — готов к работе</div>',
                    unsafe_allow_html=True)
    elif gemini_input and not rep_input:
        st.markdown('<div class="rv-status rv-status-nokey">⚠ Введите Replicate токен для генерации (r8_...)</div>',
                    unsafe_allow_html=True)
    elif rep_input and not gemini_input:
        st.markdown('<div class="rv-status rv-status-nokey">⚠ Введите Gemini ключ для анализа лица (AIza...)</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="rv-status rv-status-nokey">⚠ Введите оба ключа для активации AI</div>',
                    unsafe_allow_html=True)

    st.divider()

    # ── Sliders ──
    st.markdown('<div class="rv-card-title">⚙️ Параметры ринопластики</div>', unsafe_allow_html=True)

    rc = st.session_state.rc
    slider_defs = [
        ("hump",          "Высота горбинки (горб спинки)",  -50, 50, 0),
        ("tip_proj",      "Проекция кончика носа",          -50, 50, 0),
        ("nose_width",    "Ширина носа",                    -50, 50, 0),
        ("nostril_width", "Ширина ноздрей",                 -50, 50, 0),
        ("tip_angle",     "Угол наклона кончика",           -30, 30, 0),
        ("nose_length",   "Длина носа",                     -50, 50, 0),
    ]
    params = {}
    for skey, label, lo, hi, dflt in slider_defs:
        params[skey] = st.slider(label, lo, hi, dflt, key=f"{skey}_{rc}")

    st.divider()

    # ── Buttons ──
    btn1, btn2 = st.columns(2)
    with btn1:
        gen = st.button("✨ Analyze & Generate", type="primary",
                        use_container_width=True, key="btn_gen")
    with btn2:
        rst = st.button("🔄 Сбросить всё", use_container_width=True, key="btn_rst")

    # ── Generate ──
    if gen:
        if st.session_state.orig is None:
            st.warning("Сначала загрузите фото пациента.")
        elif not st.session_state.gemini_key:
            st.warning("Введите Gemini API ключ для анализа лица.")
        elif not st.session_state.replicate_token:
            st.warning("Введите Replicate токен для генерации изображения.")
        else:
            img_bytes = st.session_state.orig_bytes

            # Phase 1 — Gemini vision analysis
            with st.spinner("🔬 Фаза 1 — Gemini анализ лица…"):
                analysis, aerr = analyze_face(st.session_state.gemini_key, img_bytes)
            if aerr:
                st.error(f"Анализ: {aerr}")
                st.session_state.analysis_error = aerr
                analysis = None
            else:
                st.session_state.analysis = analysis
                st.session_state.analysis_error = None

            # Phase 2 — Replicate FLUX Schnell img2img
            with st.spinner("🎨 Фаза 2 — FLUX Schnell генерация (15–30 сек)…"):
                result_img, gerr = generate_with_replicate(
                    st.session_state.replicate_token, img_bytes, params, analysis
                )
            if gerr:
                st.error(f"Генерация: {gerr}")
                st.session_state.gen_error = gerr
            else:
                st.session_state.result = apply_annotations(result_img, st.session_state.annotations)
                st.session_state.gen_error = None
                st.success("✅ Готово!", icon="✅")

    # ── Reset ──
    if rst:
        for k in list(_DEFAULTS.keys()):
            st.session_state[k] = [] if k == "annotations" else (0 if k == "rc" else None)
        st.session_state.rc       = st.session_state.get("rc", 0) + 1
        st.session_state.last_name = ""
        st.rerun()

    # ── Download ──
    if st.session_state.result is not None:
        st.divider()
        fname = (st.session_state.patient_name.strip().replace(" ", "_") or "patient")
        st.download_button(
            "💾 Сохранить результат (JPG)",
            data=pil_to_bytes(st.session_state.result),
            file_name=f"rhinovision_{fname}.jpg",
            mime="image/jpeg",
            use_container_width=True,
            key="btn_dl",
        )

# ─── Before / After comparison ─────────────────────────────────────────────────
if st.session_state.orig is not None and st.session_state.result is not None:
    st.divider()
    st.markdown('<div class="rv-card-title">⚖️ Сравнение До / После — перетащите разделитель</div>',
                unsafe_allow_html=True)
    iw, ih = st.session_state.orig.size
    display_h = min(int(ih * 780 / iw), 560)
    comparison_slider(st.session_state.orig, st.session_state.result, height=display_h)

# ─── AI Analysis Results ───────────────────────────────────────────────────────
if st.session_state.analysis is not None:
    st.divider()
    with st.expander("🔬 AI Анализ лица — детальные данные", expanded=True):
        render_analysis(st.session_state.analysis)

# ─── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="rv-disclaimer">
  <strong>⚕️ Медицинский дисклеймер.</strong>
  RhinoVision Pro предназначен исключительно для иллюстративных целей и не является медицинским
  прогнозом. AI-симуляция не гарантирует результатов хирургического вмешательства.
  Все клинические решения принимаются квалифицированным хирургом индивидуально.<br>
  <span style="color:#cbd5e1">© 2025 RhinoVision Pro &nbsp;·&nbsp; Только для медицинского персонала &nbsp;·&nbsp; Powered by Gemini AI</span>
</div>
""", unsafe_allow_html=True)
