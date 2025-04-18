import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

# --- تنظیمات اولیه صفحه و تزریق CSS برای فونت و RTL ---
st.set_page_config(page_title="بازی با نمودارها", layout="wide", page_icon="📊")

# --- CSS سفارشی برای فونت فارسی و راست‌چین ---
font_name = "Vazirmatn"

# تم رنگی یکپارچه با کنتراست بالا
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');

body, h1, h2,h3, h5, h6, p, li, label, caption, .stApp {{
    direction: rtl !important;
    text-align: right !important;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
h4{{
    direction: rtl !important;
    text-align: right !important;
    font-family: '{font_name}', Tahoma, sans-serif !important;
    color: #000000 !important;
    font-weight: bold !important;
}}
/* برای جلوگیری از راست‌چین شدن المان‌های خاص نمودار یا کد */
.stCodeBlock, .stDataFrame, svg text {{
    direction: ltr !important;
    text-align: left !important;
}}
/* تنظیمات برای نمودارهای matplotlib */
svg text {{
    font-family: sans-serif !important;
}}
/* استایل‌های مینیمال برای تم ریاضی با کنتراست بالا */
.math-theme {{
    background-color: #e1f5fe;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    color: #000000;
    font-weight: bold;
    border-left: 5px solid #0288d1;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
.stButton>button {{
    background-color: #0288d1;
    color: white;
    border: none;
    border-radius: 4px;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 15px;
}}
.stTabs [data-baseweb="tab"] {{
    height: 60px;
    white-space: pre-wrap;
    background-color: #e1f5fe;
    border-radius: 4px 4px 0 0;
    gap: 1px;
    padding-top: 15px;
    padding-bottom: 15px;
    padding-left: 20px;  
    padding-right: 20px;  
    color: #000000;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
.stTabs [aria-selected="true"] {{
    background-color: #0288d1 !important;
    color: white !important;
}}
/* کلاس جدید برای توضیحات با کنتراست بالا */
.explanation-box {{
    background-color: #fff8e1;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #ffa000;
    color: #000000;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
/* کلاس برای نکات مهم */
.important-note {{
    background-color: #ffebee;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #c62828;
    color: #000000;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
/* استایل برای expander ها */
.streamlit-expanderHeader {{
    background-color: #e8f5e9;
    border-radius: 8px;
    color: #000000;
    font-weight: bold;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
/* استایل برای دکمه نمایش پاسخ */
.show-answer-btn {{
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
/* استایل برای کادر پاسخ */
.answer-box {{
    background-color: #e8f5e9;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #4CAF50;
    color: #000000;
    font-family: '{font_name}', Tahoma, sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# --- تنظیمات سبک نمودار ---
plt.style.use('seaborn-v0_8-whitegrid')
# تعریف پالت رنگ مینیمال با تم ریاضی
math_colors = ["#0288d1", "#26a69a", "#ffa000", "#e53935", "#7b1fa2"]
math_cmap = LinearSegmentedColormap.from_list("math_theme", math_colors)

# تنظیم فونت برای نمودارها
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# --- شروع محتوای برنامه ---
st.title("📊 بازی با نمودارها: چگونه نمودارها می‌توانند گمراه‌کننده باشند؟")

with st.container():
    st.markdown("""
    <div class="math-theme">
    این ابزار تعاملی به شما نشان می‌دهد که چگونه تغییرات کوچک در نحوه نمایش داده‌ها می‌تواند برداشت ما را از واقعیت تغییر دهد.
    در ریاضیات و آمار، نمودارها ابزاری قدرتمند برای انتقال اطلاعات هستند، اما می‌توانند به سادگی برای ارائه تصویری گمراه‌کننده استفاده شوند.
    </div>
    """, unsafe_allow_html=True)

# --- بخش انتخاب داده ---
# داده‌ها با نام ستون انگلیسی برای استفاده در نمودار
data_options = {
    "وزن کدو تنبل (کتاب)": pd.DataFrame({'Name': ['Ali', 'Taghi', 'Arash'], 'Weight (kg)': [10, 20, 40]}),
    "سود شرکت (کتاب)": pd.DataFrame({'Month': ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar'], 'Profit (Billion Rials)': [2.0, 2.1, 2.2, 2.1, 2.3, 2.4]}),
    "آلودگی هوا (مثال)": pd.DataFrame({'Month': ['Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'], 'AQI Index': [110, 130, 155, 160, 140, 120]}),
    "گل‌های بازیکن (مثال)": pd.DataFrame({'Season': ['S1', 'S2', 'S3', 'S4', 'S5'], 'Goals Scored': [8, 10, 9, 12, 11]}),
    "نمرات ریاضی (مثال)": pd.DataFrame({'Term': ['Term 1', 'Term 2', 'Term 3', 'Term 4'], 'Score': [17.2, 17.8, 17.5, 18.2]}),
    "مصرف انرژی (مثال)": pd.DataFrame({'Year': ['1398', '1399', '1400', '1401', '1402'], 'Consumption (kWh)': [320, 310, 305, 315, 300]})
}

# مپینگ ماه‌های فارسی به انگلیسی برای نمودارها
month_mapping = {
    'فروردین': 'Farvardin',
    'اردیبهشت': 'Ordibehesht',
    'خرداد': 'Khordad',
    'تیر': 'Tir',
    'مرداد': 'Mordad',
    'شهریور': 'Shahrivar',
    'مهر': 'Mehr',
    'آبان': 'Aban',
    'آذر': 'Azar',
    'دی': 'Dey',
    'بهمن': 'Bahman',
    'اسفند': 'Esfand'
}

# --- ایجاد ستون‌های کناری برای کنترل‌ها ---
with st.sidebar:
    # st.image("https://img.icons8.com/color/96/000000/mathematics.png", width=100)
    st.title("تنظیمات نمودار")
    
    # انتخاب مجموعه داده
    selected_data_name_fa = st.selectbox("انتخاب مجموعه داده:", list(data_options.keys()))
    df = data_options[selected_data_name_fa]
    
    # تبدیل نام‌های فارسی به انگلیسی برای نمودار
    x_col = df.columns[0]
    y_col = df.columns[1]
    
    # --- بخش کنترل محور عمودی ---
    st.header("کنترل محور عمودی (Y-Axis)")
    min_val = df[y_col].min()
    max_val = df[y_col].max()
    
    # تعیین مقدار پیش‌فرض مناسب برای شروع و پایان
    auto_y_min = 0
    auto_y_max = max_val * 1.15
    
    # بازنویسی ویجت انتخاب range برای رفع باگ
    st.markdown("### نقطه شروع و پایان محور عمودی")

    # Calculate appropriate min_value for the input
    calculated_min = float(min_val * 0.5) if min_val > 0 else float(min_val * 1.5)

    # Ensure default value is always >= min_value
    default_y_min = max(auto_y_min, calculated_min)
    
    # استفاده از number_input به جای slider برای دقت بیشتر
    y_min_manipulated = st.number_input(
        f"نقطه شروع محور عمودی (پیش‌فرض: {default_y_min})",
        min_value=calculated_min,
        max_value=float(max_val * 0.9),
        value=default_y_min,
        step=0.1 if df[y_col].dtype == 'float' else 1.0,
        key='ymin_input'
    )
    
    y_max_manipulated = st.number_input(
        f"نقطه پایان محور عمودی (پیش‌فرض: {auto_y_max:.1f})",
        min_value=float(y_min_manipulated + (0.1 if df[y_col].dtype == 'float' else 1)),
        max_value=float(max_val * 2.5),
        value=float(auto_y_max),
        step=0.1 if df[y_col].dtype == 'float' else 1.0,
        key='ymax_input'
    )
    
    # نمایش محدوده انتخاب شده
    st.markdown(f"**محدوده انتخاب شده:** از {y_min_manipulated} تا {y_max_manipulated}")
    
    # کنترل‌های اضافی برای زیبایی نمودار
    st.header("تنظیمات ظاهری")
    chart_style = st.selectbox(
        "سبک نمودار:",
        ["مینیمال", "کلاسیک", "تیره", "روشن", "رنگارنگ"]
    )
    
    show_grid = st.checkbox("نمایش خطوط راهنما", value=True)
    show_annotations = st.checkbox("نمایش مقادیر روی نمودار", value=False)

# --- تنظیم سبک نمودار بر اساس انتخاب کاربر ---
if chart_style == "مینیمال":
    plt.style.use('seaborn-v0_8-whitegrid')
    color_palette = ["#0288d1", "#26a69a"]
elif chart_style == "کلاسیک":
    plt.style.use('seaborn-v0_8')
    color_palette = ["#E63946", "#457B9D"]
elif chart_style == "تیره":
    plt.style.use('dark_background')
    color_palette = ["#BB86FC", "#03DAC5"]
elif chart_style == "روشن":
    plt.style.use('seaborn-v0_8-pastel')
    color_palette = ["#FF9F1C", "#2EC4B6"]
else:  # رنگارنگ
    plt.style.use('default')
    color_palette = ["#FF595E", "#FFCA3A"]

# --- بخش نمایش نمودارها ---
st.header("مقایسه نمودار 'صادقانه' و 'دستکاری شده'")

# تب‌بندی برای نمایش نمودارها
tabs = st.tabs(["نمودارهای مقایسه‌ای", "تحلیل تفاوت‌ها", "ترفندهای گمراه‌کننده"])

with tabs[0]:
    col1, col2 = st.columns(2)
    
    # نمودار صادقانه
    with col1:
        st.subheader("نمودار صادقانه")
        fig_honest, ax_honest = plt.subplots(figsize=(10, 6))
        
        if selected_data_name_fa in ["سود شرکت (کتاب)", "آلودگی هوا (مثال)", "نمرات ریاضی (مثال جدید)", "مصرف انرژی (مثال جدید)"]:
            ax_honest.plot(df[x_col], df[y_col], marker='o', label=y_col, color=color_palette[0], linewidth=3, markersize=8)
            if show_annotations:
                for i, val in enumerate(df[y_col]):
                    ax_honest.annotate(f'{val:.1f}', (i, val), textcoords="offset points", 
                                      xytext=(0,10), ha='center', fontsize=9,
                                      bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
        else:
            bars = ax_honest.bar(df[x_col], df[y_col], label=y_col, color=color_palette[0], width=0.6)
            if show_annotations:
                for bar in bars:
                    height = bar.get_height()
                    ax_honest.annotate(f'{height:.1f}',
                                      xy=(bar.get_x() + bar.get_width() / 2, height),
                                      xytext=(0, 3),
                                      textcoords="offset points",
                                      ha='center', va='bottom', fontsize=9,
                                      bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
        
        # تنظیمات نمودار - متون به انگلیسی
        ax_honest.set_title(f"Honest Chart: {y_col}", fontsize=14, pad=20)
        ax_honest.set_xlabel(x_col, fontsize=12, labelpad=10)
        ax_honest.set_ylabel(y_col, fontsize=12, labelpad=10)
        ax_honest.tick_params(axis='x', rotation=45, labelsize=10)
        ax_honest.tick_params(axis='y', labelsize=10)
        ax_honest.set_ylim(bottom=0)
        
        if show_grid:
            ax_honest.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            ax_honest.grid(False)
            
        plt.tight_layout()
        st.pyplot(fig_honest)
        
        with st.expander("توضیحات نمودار صادقانه"):
            st.markdown("""
            <div class="explanation-box">
            <strong>ویژگی‌های نمودار صادقانه:</strong>
            <ul>
                <li>محور عمودی از صفر شروع می‌شود</li>
                <li>مقیاس‌بندی مناسب و متناسب با داده‌ها</li>
                <li>نمایش کامل تغییرات بدون اغراق</li>
                <li>عدم حذف داده‌های مهم</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # نمودار دستکاری شده
    with col2:
        st.subheader("نمودار دستکاری شده")
        fig_manipulated, ax_manipulated = plt.subplots(figsize=(10, 6))
        
        if selected_data_name_fa in ["سود شرکت (کتاب)", "آلودگی هوا (مثال)", "نمرات ریاضی (مثال جدید)", "مصرف انرژی (مثال جدید)"]:
            ax_manipulated.plot(df[x_col], df[y_col], marker='o', label=y_col, color=color_palette[1], linewidth=3, markersize=8)
            if show_annotations:
                for i, val in enumerate(df[y_col]):
                    ax_manipulated.annotate(f'{val:.1f}', (i, val), textcoords="offset points", 
                                           xytext=(0,10), ha='center', fontsize=9,
                                           bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
        else:
            bars = ax_manipulated.bar(df[x_col], df[y_col], label=y_col, color=color_palette[1], width=0.6)
            if show_annotations:
                for bar in bars:
                    height = bar.get_height()
                    ax_manipulated.annotate(f'{height:.1f}',
                                           xy=(bar.get_x() + bar.get_width() / 2, height),
                                           xytext=(0, 3),
                                           textcoords="offset points",
                                           ha='center', va='bottom', fontsize=9,
                                           bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
        
        # تنظیمات نمودار دستکاری شده - متون به انگلیسی
        ax_manipulated.set_title(f"Manipulated Chart: {y_col}", fontsize=14, pad=20)
        ax_manipulated.set_xlabel(x_col, fontsize=12, labelpad=10)
        ax_manipulated.set_ylabel(y_col, fontsize=12, labelpad=10)
        ax_manipulated.tick_params(axis='x', rotation=45, labelsize=10)
        ax_manipulated.tick_params(axis='y', labelsize=10)
        
        # استفاده از مقادیر اسلایدر
        ax_manipulated.set_ylim(bottom=y_min_manipulated, top=y_max_manipulated)
        
        if show_grid:
            ax_manipulated.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            ax_manipulated.grid(False)
            
        plt.tight_layout()
        st.pyplot(fig_manipulated)
        
        with st.expander("توضیحات نمودار دستکاری شده"):
            st.markdown(f"""
            <div class="important-note">
            <strong>ترفندهای به کار رفته در این نمودار:</strong>
            <ul>
                <li>محور عمودی از {y_min_manipulated} (به جای صفر) شروع می‌شود</li>
                <li>محدوده نمایش تا {y_max_manipulated:.1f} محدود شده است</li>
                <li>این تغییرات باعث می‌شود تفاوت‌ها بزرگتر یا کوچکتر از واقعیت به نظر برسند</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

with tabs[1]:
    st.subheader("تحلیل تفاوت‌های دو نمودار")
    
    # محاسبه درصد تغییر ظاهری
    range_honest = max_val - 0  # محدوده نمودار صادقانه
    range_manipulated = y_max_manipulated - y_min_manipulated  # محدوده نمودار دستکاری شده
    
    # محاسبه نسبت بزرگنمایی/کوچک‌نمایی
    if range_honest > 0:
        magnification_ratio = range_honest / range_manipulated
        if magnification_ratio < 1:
            effect = "بزرگنمایی"
            magnification_percent = (1/magnification_ratio - 1) * 100
        else:
            effect = "کوچک‌نمایی"
            magnification_percent = (magnification_ratio - 1) * 100
    else:
        effect = "نامشخص"
        magnification_percent = 0
    
    # نمایش اطلاعات تحلیلی
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="math-theme">
        <h4>تأثیر تغییر مقیاس</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="explanation-box">
        <ul>
            <li><strong>محدوده نمودار صادقانه:</strong> از 0 تا {max_val:.1f}</li>
            <li><strong>محدوده نمودار دستکاری شده:</strong> از {y_min_manipulated:.1f} تا {y_max_manipulated:.1f}</li>
            <li><strong>اثر ایجاد شده:</strong> {effect} تغییرات به میزان حدود {magnification_percent:.1f}%</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="math-theme"> 
        <h4>فرمول محاسبه نسبت بزرگنمایی/کوچک‌نمایی:</h4>
        <p>نسبت = محدوده نمودار صادقانه / محدوده نمودار دستکاری شده</p>
        <p>درصد تغییر = (نسبت - 1) × 100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # نمایش تصویر مقایسه‌ای از تأثیر مقیاس
        fig_comparison = plt.figure(figsize=(8, 6))
        
        # ایجاد یک نمودار ساده برای نمایش تأثیر مقیاس
        plt.plot([1, 2], [1, 2], 'o-', color=color_palette[0], label='Real Data')
        
        # نمایش خط با مقیاس متفاوت
        if effect == "بزرگنمایی":
            plt.plot([1, 2], [1, 1 + (2-1)/magnification_ratio], 'o-', color=color_palette[1], label='Magnified View')
        else:
            plt.plot([1, 2], [1, 1 + (2-1)*magnification_ratio], 'o-', color=color_palette[1], label='Minimized View')
        
        plt.title('Effect of Scale Change on Perception')
        plt.legend(loc='best')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        st.pyplot(fig_comparison)
        
        st.markdown("""
        <div class="explanation-box">
        این نمودار نشان می‌دهد چگونه تغییر مقیاس می‌تواند درک ما از شیب تغییرات را تحت تأثیر قرار دهد.
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("ترفندهای رایج در دستکاری نمودارها")
    
    trick_tabs = st.tabs(["تغییر مقیاس", "حذف نقطه صفر", "استفاده از تصاویر", "انتخاب نوع نمودار نامناسب", "حذف داده‌های ناسازگار"])
    
    with trick_tabs[0]:
        st.markdown("""
        <div class="math-theme">
        <h4>ترفند ۱: تغییر مقیاس محور عمودی</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
        با فشرده یا کشیده کردن مقیاس محور عمودی، می‌توان تغییرات را بزرگتر یا کوچکتر از واقعیت نشان داد:
        
        <ul>
            <li><strong>فشرده کردن مقیاس:</strong> باعث می‌شود تغییرات کوچکتر به نظر برسند (مناسب برای پنهان کردن نوسانات شدید)</li>
            <li><strong>کشیده کردن مقیاس:</strong> باعث می‌شود تغییرات بزرگتر به نظر برسند (مناسب برای بزرگنمایی تغییرات کوچک)</li>
        </ul>
        
        <strong>مثال کاربرد در دنیای واقعی:</strong> شرکت‌ها برای نشان دادن رشد سود، گاهی مقیاس را طوری تنظیم می‌کنند که افزایش اندک سود، بسیار چشمگیر به نظر برسد.
        </div>
        """, unsafe_allow_html=True)
        
        # نمایش مثال تغییر مقیاس
        example_data = pd.DataFrame({
            'Month': ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar'],
            'Value': [100, 102, 101, 103, 102, 104]
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # نمودار با مقیاس عادی
        ax1.plot(example_data['Month'], example_data['Value'], 'o-', color=color_palette[0])
        ax1.set_title('Normal Scale (from zero)')
        ax1.set_ylim(0, 110)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Value')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # نمودار با مقیاس دستکاری شده
        ax2.plot(example_data['Month'], example_data['Value'], 'o-', color=color_palette[1])
        ax2.set_title('Manipulated Scale')
        ax2.set_ylim(99, 105)
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Value')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.caption("مقایسه دو نمودار با داده‌های یکسان اما مقیاس متفاوت. تغییرات در نمودار سمت راست بسیار بزرگتر به نظر می‌رسند.")
    
    with trick_tabs[1]:
        st.markdown("""
        <div class="math-theme">
        <h4>ترفند ۲: حذف نقطه صفر</h4>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explanation-box">
        شروع محور عمودی از عددی بزرگتر از صفر می‌تواند تفاوت‌ها را بزرگنمایی کند:
        
        <ul>
            <li>در نمودارهای میله‌ای، شروع از صفر اهمیت بیشتری دارد زیرا چشم ما ارتفاع کل میله را مقایسه می‌کند</li>
            <li>در نمودارهای خطی، گاهی حذف صفر برای نمایش بهتر جزئیات قابل قبول است، اما باید به وضوح مشخص شود</li>
        </ul>
        
        <strong>مثال کاربرد در دنیای واقعی:</strong> گزارش‌های اقتصادی که می‌خواهند رشد اقتصادی را بیشتر از واقعیت نشان دهند، معمولاً محور عمودی را از عددی نزدیک به کمترین مقدار شروع می‌کنند.
        </div>
        """, unsafe_allow_html=True)
        
        # مثال حذف نقطه صفر
        zero_trick_data = pd.DataFrame({
            'Year': ['1398', '1399', '1400', '1401', '1402'],
            'Index': [95, 100, 105, 110, 115]
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # نمودار با صفر
        ax1.bar(zero_trick_data['Year'], zero_trick_data['Index'], color=color_palette[0])
        ax1.set_title('Chart with Zero Baseline')
        ax1.set_ylim(0, 120)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Index')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # نمودار بدون صفر
        ax2.bar(zero_trick_data['Year'], zero_trick_data['Index'], color=color_palette[1])
        ax2.set_title('Chart without Zero Baseline')
        ax2.set_ylim(90, 120)
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Index')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.caption("در نمودار سمت راست، رشد شاخص بسیار چشمگیرتر به نظر می‌رسد، در حالی که داده‌ها یکسان هستند.")
    
    with trick_tabs[2]:
        st.markdown("""
        <div class="math-theme">
        <h4>ترفند ۳: استفاده از تصاویر گمراه‌کننده</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
        گاهی از تصاویر دو یا سه بعدی برای نمایش داده‌ها استفاده می‌شود که می‌تواند گمراه‌کننده باشد:
        
        <ul>
            <li>استفاده از تصاویر سه بعدی برای نمایش داده‌های یک بعدی</li>
            <li>استفاده از تصاویر با اندازه‌های متفاوت که به جای تغییر در یک بعد، در چند بعد تغییر می‌کنند</li>
        </ul>
        
        <strong>مثال کاربرد در دنیای واقعی:</strong> تبلیغات تجاری گاهی از تصاویر سه بعدی استفاده می‌کنند تا تفاوت محصول خود را با رقبا بزرگتر نشان دهند.
        </div>
        """, unsafe_allow_html=True)
        
        # مثال تصاویر گمراه‌کننده
        image_trick_data = pd.DataFrame({
            'Product': ['A', 'B'],
            'Sales': [100, 150]
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # نمودار ساده
        ax1.bar(image_trick_data['Product'], image_trick_data['Sales'], color=color_palette[0])
        ax1.set_title('Simple 2D Chart')
        ax1.set_ylim(0, 200)
        ax1.set_xlabel('Product')
        ax1.set_ylabel('Sales')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # نمودار سه بعدی
        ax2 = plt.subplot(1, 2, 2, projection='3d')
        ax2.bar3d([0], [0], [0], 0.5, 0.5, image_trick_data['Sales'][0], color=color_palette[0])
        ax2.bar3d([1], [0], [0], 0.5, 0.5, image_trick_data['Sales'][1], color=color_palette[1])
        ax2.set_title('3D Chart (Misleading)')
        ax2.set_zlim(0, 200)
        ax2.set_xlabel('Product')
        ax2.set_ylabel('')
        ax2.set_zlabel('Sales')
        ax2.set_xticks([0.25, 1.25])
        ax2.set_xticklabels(['A', 'B'])
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.caption("نمودار سه بعدی (سمت راست) تفاوت بین دو مقدار را بزرگتر نشان می‌دهد و درک دقیق مقادیر را دشوارتر می‌کند.")
    
    with trick_tabs[3]:
        st.markdown("""
        <div class="math-theme">
        <h4>ترفند ۴: انتخاب نوع نمودار نامناسب</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
        انتخاب نوع نمودار نامناسب برای داده‌ها می‌تواند باعث سوء تفاهم شود:
        
        <ul>
            <li>استفاده از نمودار خطی برای داده‌های گسسته بدون ارتباط زمانی</li>
            <li>استفاده از نمودار دایره‌ای برای مقایسه مقادیر زیاد</li>
            <li>استفاده از نمودار میله‌ای افقی برای سری‌های زمانی</li>
        </ul>
        
        <strong>مثال کاربرد در دنیای واقعی:</strong> گزارش‌های مالی گاهی از نمودارهای پیچیده استفاده می‌کنند تا تحلیل داده‌ها را برای مخاطب دشوارتر کنند.
        </div>
        """, unsafe_allow_html=True)
        
        # مثال نمودار نامناسب
        chart_data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D', 'E'],
            'Value': [10, 11, 13, 9, 12]
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # نمودار مناسب (میله‌ای)
        ax1.bar(chart_data['Category'], chart_data['Value'], color=color_palette[0])
        ax1.set_title('Appropriate Chart (Bar)')
        ax1.set_xlabel('Category')
        ax1.set_ylabel('Value')
        ax1.set_ylim(0, 15)
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # نمودار نامناسب (خطی برای داده‌های گسسته)
        ax2.plot(chart_data['Category'], chart_data['Value'], 'o-', color=color_palette[1])
        ax2.set_title('Inappropriate Chart (Line for Discrete Data)')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Value')
        ax2.set_ylim(0, 15)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.caption("نمودار خطی (سمت راست) برای داده‌های گسسته بدون ارتباط زمانی مناسب نیست و می‌تواند روند کاذب ایجاد کند.")
    
    with trick_tabs[4]:
        st.markdown("""
        <div class="math-theme">
        <h4>ترفند ۵: حذف داده‌های ناسازگار</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
        حذف یا پنهان کردن داده‌هایی که با روایت مورد نظر سازگار نیستند:
        
        <ul>
            <li>حذف نقاط داده‌ای که روند کلی را نقض می‌کنند</li>
            <li>شروع نمودار از نقطه‌ای خاص برای پنهان کردن بخشی از تاریخچه</li>
            <li>استفاده از میانگین به جای نمایش کل داده‌ها برای پنهان کردن پراکندگی</li>
        </ul>
        
        <strong>مثال کاربرد در دنیای واقعی:</strong> گزارش‌های اقتصادی گاهی سال‌های رکود را از تحلیل‌ها حذف می‌کنند تا تصویر مثبت‌تری ارائه دهند.
        </div>
        """, unsafe_allow_html=True)
        
        # مثال حذف داده
        omit_data = pd.DataFrame({
            'Year': ['1397', '1398', '1399', '1400', '1401', '1402'],
            'Index': [90, 70, 85, 95, 105, 110]
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # نمودار کامل
        ax1.plot(omit_data['Year'], omit_data['Index'], 'o-', color=color_palette[0])
        ax1.set_title('Complete Data')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Index')
        ax1.set_ylim(60, 120)
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # نمودار با داده حذف شده
        omit_data_filtered = omit_data[omit_data['Year'] != '1398']  # حذف سال ۱۳۹۸ که افت شدید داشته
        ax2.plot(omit_data_filtered['Year'], omit_data_filtered['Index'], 'o-', color=color_palette[1])
        ax2.set_title('Data with Omission')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Index')
        ax2.set_ylim(60, 120)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.caption("در نمودار سمت راست، سال ۱۳۹۸ که افت شدیدی در شاخص داشته حذف شده و روند کلی صعودی به نظر می‌رسد.")

# --- بخش آزمون و تمرین ---
st.header("آزمون: تشخیص نمودارهای گمراه‌کننده")
st.markdown("""
<div class="explanation-box">
در هر مورد، کدام نمودار صادقانه‌تر است و کدام یک گمراه‌کننده؟ چه ترفندی در نمودار گمراه‌کننده استفاده شده است؟
</div>
""", unsafe_allow_html=True)

# آزمون ۱
st.subheader("آزمون ۱: مقایسه فروش ماهانه")
col1, col2 = st.columns(2)

# داده آزمون ۱
quiz_data1 = pd.DataFrame({
    'Month': ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar'],
    'Sales': [980, 1020, 1050, 1030, 1080, 1100]
})

with col1:
    fig_q1a, ax_q1a = plt.subplots(figsize=(8, 5))
    ax_q1a.bar(quiz_data1['Month'], quiz_data1['Sales'], color=color_palette[0])
    ax_q1a.set_title('Chart A')
    ax_q1a.set_xlabel('Month')
    ax_q1a.set_ylabel('Sales (Million Tomans)')
    ax_q1a.set_ylim(0, 1200)
    ax_q1a.tick_params(axis='x', rotation=45)
    ax_q1a.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_q1a)

with col2:
    fig_q1b, ax_q1b = plt.subplots(figsize=(8, 5))
    ax_q1b.bar(quiz_data1['Month'], quiz_data1['Sales'], color=color_palette[1])
    ax_q1b.set_title('Chart B')
    ax_q1b.set_xlabel('Month')
    ax_q1b.set_ylabel('Sales (Million Tomans)')
    ax_q1b.set_ylim(950, 1150)
    ax_q1b.tick_params(axis='x', rotation=45)
    ax_q1b.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_q1b)

answer1 = st.radio("کدام نمودار صادقانه‌تر است؟", ["نمودار A", "نمودار B"])

# مخفی کردن پاسخ و نمایش با دکمه
show_answer1 = st.button("نمایش پاسخ", key="show_answer1")
if show_answer1:
    if answer1 == "نمودار A":
        st.success("درست است! نمودار A با شروع از صفر، تصویر واقعی‌تری از تغییرات فروش نشان می‌دهد.")
        st.markdown("""
        <div class="explanation-box">
        <strong>ترفند استفاده شده در نمودار B:</strong> حذف نقطه صفر و شروع محور عمودی از عدد 950، که باعث می‌شود تغییرات فروش بسیار بزرگتر از واقعیت به نظر برسند.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("نادرست است. نمودار B با حذف نقطه صفر، تغییرات را بزرگنمایی کرده است.")

# آزمون ۲
st.subheader("آزمون ۲: رشد اقتصادی")
col1, col2 = st.columns(2)

# داده آزمون ۲
quiz_data2 = pd.DataFrame({
    'Year': ['1398', '1399', '1400', '1401', '1402'],
    'Growth': [2.1, 1.8, -0.5, 1.2, 2.5]
})

with col1:
    fig_q2a, ax_q2a = plt.subplots(figsize=(8, 5))
    ax_q2a.plot(quiz_data2['Year'], quiz_data2['Growth'], 'o-', color=color_palette[0])
    ax_q2a.set_title('Chart A')
    ax_q2a.set_xlabel('Year')
    ax_q2a.set_ylabel('Economic Growth (%)')
    ax_q2a.set_ylim(-1, 3)
    ax_q2a.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_q2a)

with col2:
    # حذف داده منفی
    quiz_data2_filtered = quiz_data2[quiz_data2['Growth'] > 0]
    
    fig_q2b, ax_q2b = plt.subplots(figsize=(8, 5))
    ax_q2b.plot(quiz_data2_filtered['Year'], quiz_data2_filtered['Growth'], 'o-', color=color_palette[1])
    ax_q2b.set_title('Chart B')
    ax_q2b.set_xlabel('Year')
    ax_q2b.set_ylabel('Economic Growth (%)')
    ax_q2b.set_ylim(0, 3)
    ax_q2b.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_q2b)

answer2 = st.radio("کدام نمودار صادقانه‌تر است؟", ["نمودار A", "نمودار B"], key="quiz2")

# مخفی کردن پاسخ و نمایش با دکمه
show_answer2 = st.button("نمایش پاسخ", key="show_answer2")
if show_answer2:
    if answer2 == "نمودار A":
        st.success("درست است! نمودار A تمام داده‌ها را نشان می‌دهد، از جمله رشد منفی در سال ۱۴۰۰.")
        st.markdown("""
        <div class="explanation-box">
        <strong>ترفند استفاده شده در نمودار B:</strong> حذف داده‌های ناسازگار (رشد منفی) که باعث می‌شود تصویر کلی مثبت‌تر به نظر برسد.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("نادرست است. نمودار B با حذف داده منفی (سال ۱۴۰۰)، تصویر گمراه‌کننده‌ای ارائه می‌دهد.")

# آزمون ۳
st.subheader("آزمون ۳: توزیع بودجه")
col1, col2 = st.columns(2)

# داده آزمون ۳
quiz_data3 = pd.DataFrame({
    'Group': ['A', 'B', 'C'],
    'Percent': [30, 35, 35]
})

with col1:
    fig_q3a, ax_q3a = plt.subplots(figsize=(8, 5))
    ax_q3a.pie(quiz_data3['Percent'], labels=quiz_data3['Group'], autopct='%1.1f%%', 
              colors=[color_palette[0], color_palette[1], "#9C27B0"])
    ax_q3a.set_title('Chart A')
    plt.tight_layout()
    st.pyplot(fig_q3a)

with col2:
    fig_q3b, ax_q3b = plt.subplots(figsize=(8, 5))
    ax_q3b.pie(quiz_data3['Percent'], labels=quiz_data3['Group'], autopct='%1.1f%%', 
              colors=[color_palette[0], color_palette[1], "#9C27B0"],
              explode=[0, 0.2, 0])  # برجسته کردن گروه B
    ax_q3b.set_title('Chart B')
    plt.tight_layout()
    st.pyplot(fig_q3b)

answer3 = st.radio("کدام نمودار صادقانه‌تر است؟", ["نمودار A", "نمودار B"], key="quiz3")

# مخفی کردن پاسخ و نمایش با دکمه
show_answer3 = st.button("نمایش پاسخ", key="show_answer3")
if show_answer3:
    if answer3 == "نمودار A":
        st.success("درست است! نمودار A تمام بخش‌ها را به طور یکسان نمایش می‌دهد.")
        st.markdown("""
        <div class="explanation-box">
        <strong>ترفند استفاده شده در نمودار B:</strong> برجسته کردن یک بخش خاص (explode) که باعث می‌شود آن بخش مهم‌تر به نظر برسد، در حالی که درصد واقعی تغییری نکرده است.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("نادرست است. نمودار B با برجسته کردن بخش B، توجه بیشتری به آن جلب می‌کند و می‌تواند گمراه‌کننده باشد.")


# --- پاورقی ---
st.markdown("""
<div style="margin-top: 50px; padding: 15px; border-top: 1px solid #ddd; text-align: center; font-size: 1.2em; color: #000000; font-weight: bold; font-family: 'Vazirmatn', Tahoma, sans-serif !important;">
این ابزار آموزشی برای درک بهتر نمودارها و تفسیر صحیح داده‌ها، توسط امیر جلوگیر دبیر ریاضی مقطع متوسطه دوم شهرستان سرایان طراحی شده است.
</div>
""", unsafe_allow_html=True)