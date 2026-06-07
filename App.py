import streamlit as st
import pandas as pd
import numpy as np
import joblib
import bisect
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Prediksi Stunting Balita",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════
# GLOBAL CSS — PREMIUM WHITE × BLUE
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

:root {
    --bg:        #ffffff;
    --bg-subtle: #f8faff;
    --bg-wash:   #eef3ff;
    --b950: #060f2e; --b900: #0d1f5c; --b800: #1a3480; --b700: #1e4db7;
    --b600: #2563eb; --b500: #3b82f6; --b400: #60a5fa; --b300: #93c5fd;
    --b200: #bfdbfe; --b100: #dbeafe; --b50:  #eff6ff;
    --t1: #060f2e; --t2: #1a3480; --t3: #475569; --t4: #94a3b8; --t5: #cbd5e1;
    --green:   #059669; --green-l: #d1fae5;
    --yellow:  #b45309; --yellow-l:#fef3c7;
    --orange:  #c2410c; --orange-l:#ffedd5;
    --red:     #b91c1c; --red-l:   #fee2e2;
    --teal:    #0e7490;
    --card:   #ffffff;
    --border: rgba(37,99,235,.12);
    --border-m: rgba(37,99,235,.22);
    --shadow-xs: 0 1px 2px rgba(14,31,92,.04);
    --shadow-sm: 0 2px 8px rgba(14,31,92,.07), 0 1px 2px rgba(0,0,0,.04);
    --shadow-md: 0 4px 20px rgba(14,31,92,.10), 0 2px 6px rgba(0,0,0,.04);
    --shadow-lg: 0 12px 40px rgba(14,31,92,.14), 0 4px 12px rgba(0,0,0,.06);
    --shadow-blue: 0 8px 32px rgba(37,99,235,.22);
    --r-sm: 8px; --r-md: 14px; --r-lg: 20px; --r-xl: 28px;
}

html,body,[class*="css"],.stApp,.main,
div[data-testid="stAppViewContainer"],
div[data-testid="stMain"]{
    font-family:'DM Sans',sans-serif!important;
    background:#f7f9ff!important;
    color:var(--t1)!important;
}

div[data-testid="stAppViewContainer"]{
    background-color:#f7f9ff!important;
    background-image:
        radial-gradient(circle, rgba(37,99,235,.13) 1.2px, transparent 1.2px),
        radial-gradient(ellipse 55% 40% at 92% 8%, rgba(59,130,246,.09) 0%, transparent 70%),
        radial-gradient(ellipse 45% 35% at 5% 92%, rgba(99,102,241,.07) 0%, transparent 70%),
        linear-gradient(180deg,
            rgba(37,99,235,.04) 0px, rgba(37,99,235,.04) 1px,
            transparent 1px, transparent 120px,
            rgba(37,99,235,.025) 120px, rgba(37,99,235,.025) 121px,
            transparent 121px
        )!important;
    background-size: 28px 28px, 100% 100%, 100% 100%, 100% 100%!important;
    background-attachment: fixed!important;
}

div[data-testid="stMain"]{ position:relative!important; }
div[data-testid="stMain"]::before{
    content:'';
    position:fixed; top:0;left:0;right:0;bottom:0;
    pointer-events:none; z-index:0;
    background-image:
        radial-gradient(circle at 96% 6%, transparent 48px, rgba(37,99,235,.08) 49px, rgba(37,99,235,.08) 54px, transparent 55px),
        radial-gradient(circle at 96% 6%, transparent 66px, rgba(37,99,235,.05) 67px, rgba(37,99,235,.05) 72px, transparent 73px),
        radial-gradient(circle at 4% 94%, transparent 38px, rgba(99,102,241,.07) 39px, rgba(99,102,241,.07) 44px, transparent 45px),
        radial-gradient(circle at 4% 94%, transparent 58px, rgba(99,102,241,.045) 59px, rgba(99,102,241,.045) 64px, transparent 65px),
        radial-gradient(circle at 2% 45%, rgba(37,99,235,.1) 4px, transparent 5px),
        radial-gradient(circle at 3.2% 48%, rgba(37,99,235,.07) 3px, transparent 4px),
        radial-gradient(circle at 1.8% 51%, rgba(99,102,241,.08) 2.5px, transparent 3.5px),
        radial-gradient(circle at 98% 55%, rgba(37,99,235,.09) 4px, transparent 5px),
        radial-gradient(circle at 96.8% 58%, rgba(37,99,235,.06) 3px, transparent 4px),
        radial-gradient(circle at 97.5% 61%, rgba(99,102,241,.07) 2.5px, transparent 3.5px),
        radial-gradient(circle at 8% 18%, rgba(37,99,235,.07) 2px, transparent 3px),
        radial-gradient(circle at 10% 22%, rgba(37,99,235,.06) 2px, transparent 3px),
        radial-gradient(circle at 12% 26%, rgba(37,99,235,.05) 1.5px, transparent 2.5px),
        radial-gradient(circle at 88% 78%, rgba(99,102,241,.07) 2px, transparent 3px),
        radial-gradient(circle at 90% 82%, rgba(99,102,241,.06) 2px, transparent 3px),
        radial-gradient(circle at 92% 86%, rgba(99,102,241,.05) 1.5px, transparent 2.5px);
    background-size:100% 100%;
    background-repeat:no-repeat;
}

.block-container > *{position:relative;z-index:1;}

#MainMenu,footer,header{visibility:hidden!important;}
.block-container{
    padding:0 1.8rem 5rem!important;
    max-width:900px!important;
}

.hero{
    position:relative; margin-bottom:0;
    padding:3.5rem 3rem 3.2rem;
    background:#ffffff;
    border-radius:var(--r-xl);
    border:1.5px solid var(--b200);
    box-shadow:var(--shadow-lg);
    overflow:hidden;
    animation:slideUp .65s cubic-bezier(.16,1,.3,1) both;
}
.hero::before{
    content:'';
    position:absolute;top:0;left:0;right:0;height:4px;
    background:linear-gradient(90deg,var(--b800),var(--b600),var(--b400));
}
.hero::after{
    content:'';
    position:absolute;inset:0;
    background-image:radial-gradient(circle,var(--b200) 1px,transparent 1px);
    background-size:28px 28px;
    opacity:.35;
    pointer-events:none;
}
.hero-inner{position:relative;z-index:1;}
.hero-pill{
    display:inline-flex;align-items:center;gap:.5rem;
    background:var(--b50);
    border:1.5px solid var(--b200);
    color:var(--b700);
    font-size:.65rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
    padding:.3rem 1rem;border-radius:100px;
    margin-bottom:1.5rem;
}
.hero-pill-dot{
    width:6px;height:6px;border-radius:50%;
    background:var(--b600);
    box-shadow:0 0 0 3px rgba(37,99,235,.2);
    animation:pulse 2s ease-in-out infinite;
}
.hero-title{
    font-family:'DM Serif Display',serif!important;
    font-size:3rem!important;font-weight:400!important;
    letter-spacing:-.03em!important;line-height:1.05!important;
    color:var(--b900)!important;
    margin:0 0 .6rem!important;
}
.hero-title em{ font-style:italic; color:var(--b600); }
.hero-divider{
    width:3rem;height:2px;
    background:linear-gradient(90deg,var(--b600),var(--b300));
    border-radius:2px;
    margin:.9rem 0;
}
.hero-sub{
    font-size:.84rem!important;
    color:var(--t3)!important;
    font-weight:400!important;
    line-height:1.7!important;
    margin:0!important;
    letter-spacing:.01em;
}

div[data-testid="stTabs"] [role="tablist"]{
    gap:.3rem;
    border-bottom:2px solid var(--b100)!important;
    background:#ffffff!important;
    padding:.5rem .5rem 0!important;
    border-radius:var(--r-md) var(--r-md) 0 0!important;
    margin-bottom:1.8rem;
}
div[data-testid="stTabs"] [role="tab"]{
    background:transparent!important;
    border:none!important;
    color:var(--t4)!important;
    font-family:'DM Sans',sans-serif!important;
    font-size:.8rem!important;
    font-weight:500!important;
    padding:.55rem 1.3rem!important;
    border-radius:var(--r-sm) var(--r-sm) 0 0!important;
    letter-spacing:.01em!important;
    transition:all .15s!important;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"]{
    background:var(--b50)!important;
    color:var(--b700)!important;
    border-bottom:2.5px solid var(--b600)!important;
    font-weight:600!important;
}
div[data-testid="stTabs"] [role="tab"]:hover{
    color:var(--b600)!important;
    background:var(--bg-wash)!important;
}

.slabel{
    font-size:.62rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
    color:var(--b600);display:flex;align-items:center;gap:.8rem;
    margin:2rem 0 1.2rem;
}
.slabel::before{
    content:'';
    width:3px;height:14px;
    background:linear-gradient(180deg,var(--b600),var(--b300));
    border-radius:2px;flex-shrink:0;
}
.slabel::after{
    content:'';flex:1;height:1px;
    background:linear-gradient(90deg,var(--b100),transparent);
}

div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stSelectbox"]>div>div{
    background:#ffffff!important;
    border:1.5px solid var(--b100)!important;
    border-radius:var(--r-sm)!important;
    color:var(--t1)!important;
    font-family:'DM Sans',sans-serif!important;
    font-size:.9rem!important;
    box-shadow:var(--shadow-xs)!important;
    transition:border-color .15s,box-shadow .15s!important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stDateInput"] input:focus,
div[data-testid="stSelectbox"]>div>div:focus-within{
    border-color:var(--b500)!important;
    box-shadow:0 0 0 3px rgba(59,130,246,.13)!important;
    outline:none!important;
}
div[data-testid="stSelectbox"] ul{
    background:#ffffff!important;
    border:1.5px solid var(--b100)!important;
    border-radius:var(--r-md)!important;
    padding:.4rem!important;
    box-shadow:var(--shadow-md)!important;
}
div[data-testid="stSelectbox"] li{
    border-radius:var(--r-sm)!important;
    color:var(--t2)!important;
    font-family:'DM Sans',sans-serif!important;
}
div[data-testid="stSelectbox"] li:hover{
    background:var(--b50)!important;
    color:var(--b700)!important;
}
label[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] p{
    color:var(--t3)!important;
    font-size:.7rem!important;
    font-weight:600!important;
    letter-spacing:.1em!important;
    text-transform:uppercase!important;
    font-family:'DM Sans',sans-serif!important;
}
div[data-testid="stNumberInput"] button{
    background:var(--bg-subtle)!important;
    border:1px solid var(--b100)!important;
    color:var(--t3)!important;
    border-radius:6px!important;
}

.stButton>button{
    width:100%!important;
    background:var(--b700)!important;
    color:#ffffff!important;
    border:none!important;
    border-radius:var(--r-md)!important;
    padding:.9rem 2rem!important;
    font-size:.83rem!important;
    font-weight:600!important;
    letter-spacing:.08em!important;
    text-transform:uppercase!important;
    font-family:'DM Sans',sans-serif!important;
    box-shadow:0 4px 16px rgba(30,77,183,.3)!important;
    transition:all .2s ease!important;
    position:relative!important;
    overflow:hidden!important;
}
.stButton>button::before{
    content:'';
    position:absolute;inset:0;
    background:linear-gradient(135deg,rgba(255,255,255,.12) 0%,transparent 60%);
    pointer-events:none;
}
.stButton>button:hover{
    transform:translateY(-2px)!important;
    background:var(--b800)!important;
    box-shadow:0 8px 28px rgba(30,77,183,.38)!important;
}
.stButton>button:active{ transform:translateY(0)!important; }

.rcard{
    border-radius:var(--r-xl);
    padding:2.4rem 2.2rem;
    text-align:center;
    position:relative;
    overflow:hidden;
    margin-bottom:1.2rem;
    box-shadow:var(--shadow-lg);
    border:1.5px solid transparent;
    animation:popIn .5s cubic-bezier(.34,1.56,.64,1) both;
}
.rcard::before{
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:var(--accent-bar);
}
.rcard::after{
    content:'';position:absolute;inset:0;
    background:radial-gradient(ellipse 60% 50% at 50% -5%,var(--glow),transparent 65%);
    pointer-events:none;
}
.rc-n{
    background:linear-gradient(160deg,#f0fdf8 0%,#ecfdf5 60%,#d1fae5 100%);
    border-color:rgba(5,150,105,.2);
    --glow:rgba(5,150,105,.15);
    --accent-bar:linear-gradient(90deg,#059669,#34d399);
}
.rc-w{
    background:linear-gradient(160deg,#fffbeb 0%,#fef9ee 60%,#fef3c7 100%);
    border-color:rgba(180,83,9,.2);
    --glow:rgba(217,119,6,.15);
    --accent-bar:linear-gradient(90deg,#b45309,#f59e0b);
}
.rc-s{
    background:linear-gradient(160deg,#fff7f0 0%,#fff4ed 60%,#ffedd5 100%);
    border-color:rgba(194,65,12,.2);
    --glow:rgba(234,88,12,.15);
    --accent-bar:linear-gradient(90deg,#c2410c,#f97316);
}
.rc-t{
    background:linear-gradient(160deg,#fff1f2 0%,#fef2f2 60%,#fee2e2 100%);
    border-color:rgba(185,28,28,.2);
    --glow:rgba(220,38,38,.15);
    --accent-bar:linear-gradient(90deg,#b91c1c,#ef4444);
}
.rc-eye{
    font-size:.6rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
    opacity:.6;margin-bottom:.7rem;position:relative;z-index:1;
    font-family:'DM Sans',sans-serif;
}
.rc-ico{font-size:2.4rem;margin-bottom:.3rem;position:relative;z-index:1;line-height:1;}
.rc-ttl{
    font-family:'DM Serif Display',serif;
    font-size:2.2rem;font-weight:400;letter-spacing:-.025em;line-height:1;
    margin-bottom:.45rem;position:relative;z-index:1;
}
.rc-sub{font-size:.82rem;opacity:.6;position:relative;z-index:1;}

.conf-wrap{
    background:#ffffff;
    border:1.5px solid var(--b100);
    border-radius:var(--r-lg);
    padding:1.3rem;
    margin-bottom:1rem;
    display:flex;align-items:center;gap:1.2rem;
    box-shadow:var(--shadow-sm);
}
.conf-ring{
    width:68px;height:68px;border-radius:50%;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    background:conic-gradient(var(--rc) var(--pct),var(--b100) 0);
    position:relative;
}
.conf-ring::before{
    content:'';position:absolute;inset:10px;border-radius:50%;
    background:#ffffff;box-shadow:inset 0 1px 4px rgba(0,0,0,.06);
}
.conf-ring span{position:relative;z-index:1;font-size:.88rem;font-weight:600;}
.conf-lbl{font-size:.59rem;letter-spacing:.15em;text-transform:uppercase;color:var(--t4);font-weight:600;margin-bottom:.3rem;}
.conf-val{font-family:'DM Serif Display',serif;font-size:1.5rem;font-weight:400;line-height:1;margin-bottom:.2rem;}
.conf-desc{font-size:.73rem;color:var(--t3);}

.gauge{
    background:#ffffff;border:1.5px solid var(--b100);
    border-radius:var(--r-lg);padding:1.3rem 1.5rem;
    margin-bottom:1rem;box-shadow:var(--shadow-sm);
}
.gtop{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.9rem;}
.gttl{font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;font-weight:600;color:var(--t4);}
.gnum{font-family:'DM Serif Display',serif;font-size:1.6rem;font-weight:400;}
.gtrack{height:8px;border-radius:100px;background:var(--b100);position:relative;}
.gfill{
    position:absolute;left:0;top:0;height:100%;border-radius:100px;width:100%;
    background:linear-gradient(90deg,#059669 0%,#f59e0b 35%,#f97316 65%,#ef4444 100%);
}
.gpip{
    position:absolute;top:50%;transform:translate(-50%,-50%);
    width:16px;height:16px;border-radius:50%;
    border:2.5px solid #ffffff;z-index:2;
    box-shadow:0 2px 8px rgba(0,0,0,.2),0 0 0 2px currentColor;
    transition:left .3s ease;
}
.gtick{display:flex;justify-content:space-between;margin-top:.55rem;font-size:.63rem;color:var(--t4);}

.zrow{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem;margin-bottom:.7rem;}
.zcard{
    background:#ffffff;
    border:1.5px solid var(--b100);
    border-radius:var(--r-lg);
    padding:1.4rem 1.1rem;
    text-align:center;
    transition:all .2s cubic-bezier(.16,1,.3,1);
    box-shadow:var(--shadow-sm);
}
.zcard:hover{
    border-color:var(--b400);
    transform:translateY(-4px);
    box-shadow:var(--shadow-md);
}
.ztag{
    font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;
    font-weight:600;color:var(--t4);margin-bottom:.55rem;
}
.zval{
    font-family:'DM Serif Display',serif;
    font-size:2.8rem;font-weight:400;line-height:1;margin-bottom:.3rem;
}
.zdesc{font-size:.67rem;color:var(--t3);margin-bottom:.5rem;}
.zbadge{
    font-size:.68rem;font-weight:600;
    padding:.24rem .75rem;border-radius:100px;
    display:inline-block;
}

.iband{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1.2rem;}
.ibox{
    background:#ffffff;
    border:1.5px solid var(--b100);
    border-radius:var(--r-md);
    padding:1.1rem .9rem;
    text-align:center;
    transition:all .2s;
    box-shadow:var(--shadow-sm);
}
.ibox:hover{border-color:var(--b300);transform:translateY(-2px);box-shadow:var(--shadow-md);}
.ibox-lbl{font-size:.57rem;letter-spacing:.12em;text-transform:uppercase;color:var(--t4);font-weight:600;margin-bottom:.4rem;}
.ibox-val{font-family:'DM Serif Display',serif;font-size:1.35rem;font-weight:400;line-height:1;margin-bottom:.2rem;color:var(--t1);}
.ibox-sub{font-size:.63rem;color:var(--t4);}

.recbox{
    background:#ffffff;
    border:1.5px solid var(--b100);
    border-left:4px solid;
    border-radius:var(--r-md);
    padding:1.2rem 1.4rem;
    margin-bottom:1rem;
    box-shadow:var(--shadow-sm);
}
.rec-head{font-size:.61rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;margin-bottom:.8rem;}
.rec-item{
    display:flex;align-items:flex-start;gap:.6rem;
    margin:.3rem 0;font-size:.84rem;color:var(--t2);
    line-height:1.6;
}
.rec-item::before{
    content:'›';color:var(--b500);flex-shrink:0;
    font-size:1.1rem;line-height:1.4;font-weight:700;
}

.ftable{
    width:100%;border-collapse:separate;border-spacing:0;
    border-radius:var(--r-lg);overflow:hidden;
    border:1.5px solid var(--b100);margin-top:.9rem;
    box-shadow:var(--shadow-sm);
}
.ftable thead tr{background:var(--b800);}
.ftable th{
    padding:.75rem 1rem;font-size:.65rem;
    color:rgba(255,255,255,.85);font-weight:600;
    letter-spacing:.1em;text-transform:uppercase;text-align:left;
    font-family:'DM Sans',sans-serif;
}
.ftable td{
    padding:.72rem 1rem;font-size:.83rem;
    color:var(--t2);border-top:1px solid var(--b50);
    background:#ffffff;
}
.ftable tr:nth-child(even) td{background:var(--bg-subtle);}
.ftable tr:hover td{background:var(--b50);}

.mrow{display:grid;grid-template-columns:repeat(5,1fr);gap:.8rem;margin-bottom:1.5rem;}
.mcard{
    background:#ffffff;
    border:1.5px solid var(--b100);
    border-radius:var(--r-md);
    padding:1.3rem .9rem;text-align:center;
    box-shadow:var(--shadow-sm);
    position:relative;overflow:hidden;
    transition:all .2s;
}
.mcard::before{
    content:'';position:absolute;bottom:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,var(--b700),var(--b400));
}
.mcard:hover{transform:translateY(-3px);box-shadow:var(--shadow-md);}
.mcard-val{
    font-family:'DM Serif Display',serif;
    font-size:1.9rem;font-weight:400;line-height:1;
    color:var(--b800);margin-bottom:.3rem;
}
.mcard-lbl{font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--t4);}

.interpbox{
    background:#ffffff;border:1.5px solid var(--b100);
    border-left:4px solid var(--b500);
    border-radius:var(--r-md);padding:1.2rem 1.4rem;
    margin-bottom:1rem;box-shadow:var(--shadow-sm);
}
.interp-ttl{
    font-size:.61rem;letter-spacing:.15em;text-transform:uppercase;
    color:var(--b700);font-weight:700;margin-bottom:.8rem;
}
.interp-row{
    display:flex;align-items:center;gap:.75rem;
    padding:.42rem .6rem;border-radius:var(--r-sm);
    margin-bottom:.22rem;font-size:.83rem;
    border:1px solid transparent;
    transition:background .15s;
}
.interp-row.active{border:1px solid;background:var(--b50);}
.interp-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}

div[data-testid="stAlert"]{
    background:#fef9c3 !important;
    border:1.5px solid #facc15 !important;
    border-radius:12px !important;
    color:#92400e !important;
    font-weight:600 !important;
    box-shadow:var(--shadow-sm) !important;
}
div[data-testid="stAlert"] p{ color:#92400e !important; }

.block-container::after{
    content:'';
    position:fixed;
    bottom:60px;right:30px;
    width:120px;height:120px;
    background:
        linear-gradient(135deg,
            rgba(37,99,235,.06) 0%,
            rgba(96,165,250,.04) 50%,
            transparent 100%);
    border:1px solid rgba(37,99,235,.1);
    border-radius:24px;
    transform:rotate(45deg);
    pointer-events:none;
    z-index:0;
    animation:floatDiamond 6s ease-in-out infinite;
}

.zcard,.ibox,.mcard{
    background-image:
        radial-gradient(circle, rgba(37,99,235,.035) 1px, transparent 1px)!important;
    background-size:20px 20px!important;
    background-color:#ffffff!important;
}

div[data-testid="stAppViewContainer"]::before{
    content:'';
    position:fixed;
    top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,
        transparent 0%,
        rgba(37,99,235,.6) 20%,
        rgba(59,130,246,.9) 50%,
        rgba(96,165,250,.7) 80%,
        transparent 100%);
    z-index:9999;
    pointer-events:none;
}

@keyframes slideUp{
    from{opacity:0;transform:translateY(-20px);}
    to{opacity:1;transform:translateY(0);}
}
@keyframes popIn{
    from{opacity:0;transform:scale(.92);}
    to{opacity:1;transform:scale(1);}
}
@keyframes pulse{
    0%,100%{box-shadow:0 0 0 3px rgba(37,99,235,.2);}
    50%{box-shadow:0 0 0 6px rgba(37,99,235,.08);}
}
@keyframes floatDiamond{
    0%,100%{transform:rotate(45deg) translateY(0);}
    50%{transform:rotate(45deg) translateY(-10px);}
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# WHO TABLES
# ══════════════════════════════════════════════
WFA_BOYS = [
    [0,0.3487,3.3464,0.14602],[1,0.2297,4.4709,0.13395],[2,0.1970,5.5675,0.12385],
    [3,0.1738,6.3762,0.11578],[4,0.1553,7.0023,0.10943],[5,0.1395,7.5105,0.10452],
    [6,0.1257,7.9340,0.10079],[7,0.1134,8.3030,0.09816],[8,0.1021,8.6420,0.09578],
    [9,0.0917,8.9496,0.09400],[10,0.0820,9.2422,0.09230],[11,0.0730,9.5238,0.09117],
    [12,0.0648,9.7870,0.09026],[15,0.0427,10.5244,0.08900],[18,0.0234,11.1945,0.08934],
    [24,-0.0108,12.4237,0.09258],[30,-0.0419,13.5638,0.09803],[36,-0.0705,14.6612,0.10456],
    [42,-0.0969,15.7243,0.11151],[48,-0.1213,16.7836,0.11856],[54,-0.1440,17.8740,0.12548],
    [60,-0.1650,19.0074,0.13208]
]
WFA_GIRLS = [
    [0,0.3809,3.2322,0.14171],[1,0.1714,4.1873,0.13724],[2,0.0962,5.1282,0.13000],
    [3,0.0569,5.8458,0.12516],[6,0.0150,7.2970,0.11556],[9,-0.0093,8.2003,0.11329],
    [12,-0.0315,8.9481,0.11382],[15,-0.0517,9.6792,0.11678],[18,-0.0702,10.3409,0.12012],
    [24,-0.1033,11.6031,0.12659],[30,-0.1323,12.8089,0.13326],[36,-0.1578,13.9348,0.13921],
    [42,-0.1802,15.0021,0.14441],[48,-0.1995,16.0586,0.14910],[54,-0.2163,17.1305,0.15331],
    [60,-0.2308,18.2298,0.15705]
]
WFL_BOYS = [
    [45.0,-0.3521,2.441,0.09182],[50.0,-0.3521,3.223,0.08221],[55.0,-0.3521,4.313,0.07654],
    [60.0,-0.3521,5.625,0.07495],[65.0,-0.3521,6.942,0.07651],[70.0,-0.3521,8.102,0.08058],
    [75.0,-0.3521,9.077,0.08648],[80.0,-0.3521,9.910,0.09376],[85.0,-0.3521,10.647,0.10163],
    [90.0,-0.3521,11.349,0.10933],[95.0,-0.3521,12.062,0.11649],[100.0,-0.3521,12.816,0.12325],
    [105.0,-0.3521,13.646,0.13012],[110.0,-0.3521,14.546,0.13741]
]
WFL_GIRLS = [
    [45.0,-0.3833,2.460,0.09029],[50.0,-0.3833,3.220,0.08007],[55.0,-0.3833,4.247,0.07228],
    [60.0,-0.3833,5.411,0.06818],[65.0,-0.3833,6.540,0.06720],[70.0,-0.3833,7.543,0.06840],
    [75.0,-0.3833,8.407,0.07120],[80.0,-0.3833,9.174,0.07548],[85.0,-0.3833,9.894,0.08111],
    [90.0,-0.3833,10.635,0.08798],[95.0,-0.3833,11.425,0.09601],[100.0,-0.3833,12.252,0.10485],
    [105.0,-0.3833,13.140,0.11447],[110.0,-0.3833,14.093,0.12490]
]
HFA_BOYS = [
    [0,43.6,46.1,49.9,53.7,56.2],[3,55.3,57.6,61.4,65.2,67.6],[6,61.7,64.2,67.6,71.6,74.0],
    [9,66.5,68.9,72.3,76.5,78.9],[12,70.5,73.1,75.7,80.5,83.0],[18,75.7,78.8,82.3,86.8,89.9],
    [24,80.0,83.3,87.1,91.9,95.2],[30,83.7,87.4,91.4,96.2,99.8],[36,86.4,90.2,94.9,101.4,103.6],
    [42,89.2,93.1,98.1,103.3,107.2],[48,92.5,96.3,101.5,107.6,111.4],[54,95.7,99.6,104.9,111.0,114.9],
    [60,98.7,102.8,108.2,114.3,118.2]
]
HFA_GIRLS = [
    [0,43.6,45.6,49.1,52.9,55.6],[3,53.5,55.6,59.8,64.0,66.1],[6,60.5,62.5,65.7,69.8,72.3],
    [9,64.6,67.1,70.1,74.7,77.2],[12,68.9,71.4,74.0,78.8,81.5],[18,74.4,77.2,80.7,86.0,88.8],
    [24,78.7,81.7,85.7,90.3,93.3],[30,82.9,86.2,90.3,95.0,98.4],[36,86.6,90.1,94.4,99.1,102.5],
    [42,90.2,94.0,98.4,103.5,107.0],[48,93.8,97.6,102.7,107.8,111.6],[54,97.2,101.1,106.4,112.0,115.8],
    [60,100.3,104.7,110.0,115.9,119.7]
]

# ══════════════════════════════════════════════
# UMUR — DIHITUNG DARI TANGGAL LAHIR & PENGUKURAN
# ══════════════════════════════════════════════
def hitung_umur_bulan(tgl_lahir, tgl_ukur):
    """Umur penuh dalam bulan (completed months) sesuai Permenkes/e-PPGBM."""
    if tgl_ukur < tgl_lahir:
        return None
    rd = relativedelta(tgl_ukur, tgl_lahir)
    return rd.years * 12 + rd.months

# ══════════════════════════════════════════════
# Z-SCORE FUNCTIONS (WHO 2006)
# ══════════════════════════════════════════════
def lms_z(X, L, M, S):
    z = ((X/M)**L - 1)/(L*S) if L != 0 else np.log(X/M)/S
    if z > 3:
        SD3 = M*(1+L*S*3)**(1/L); SD23 = SD3 - M*(1+L*S*2)**(1/L)
        z = 3 + (X-SD3)/SD23 if SD23 else 3
    elif z < -3:
        SD3 = M*(1+L*S*(-3))**(1/L); SD23 = M*(1+L*S*(-2))**(1/L) - SD3
        z = -3 + (X-SD3)/SD23 if SD23 else -3
    return round(z, 2)

def _ilms_age(age, tbl):
    ages=[r[0] for r in tbl]; a=max(0,min(60,int(round(age))))
    idx=bisect.bisect_left(ages,a)
    if idx>=len(tbl): idx=len(tbl)-1
    elif idx>0 and ages[idx]!=a:
        a0,a1=ages[idx-1],ages[idx]; t=(a-a0)/(a1-a0) if a1!=a0 else 0
        return tuple(tbl[idx-1][i]+t*(tbl[idx][i]-tbl[idx-1][i]) for i in range(1,4))
    return tbl[idx][1],tbl[idx][2],tbl[idx][3]

def _ilms_h(h, tbl):
    hs=[r[0] for r in tbl]; h=max(hs[0],min(hs[-1],h))
    idx=bisect.bisect_left(hs,h)
    if idx>=len(tbl): idx=len(tbl)-1
    elif idx>0:
        h0,h1=hs[idx-1],hs[idx]; t=(h-h0)/(h1-h0) if h1!=h0 else 0
        return tuple(tbl[idx-1][i]+t*(tbl[idx][i]-tbl[idx-1][i]) for i in range(1,4))
    return tbl[idx][1],tbl[idx][2],tbl[idx][3]

def _ihfa(age, tbl):
    ages=[r[0] for r in tbl]; a=max(0,min(60,age))
    idx=bisect.bisect_left(ages,a)
    if idx>=len(tbl): idx=len(tbl)-1
    elif idx>0 and ages[idx]!=a:
        a0,a1=ages[idx-1],ages[idx]; t=(a-a0)/(a1-a0) if a1!=a0 else 0
        return tuple(tbl[idx-1][i]+t*(tbl[idx][i]-tbl[idx-1][i]) for i in range(1,6))
    return tuple(tbl[idx][1:6])

def calc_bbu(w, age, sex):
    L,M,S=_ilms_age(age, WFA_BOYS if sex=='L' else WFA_GIRLS)
    return lms_z(w,L,M,S)

def calc_bbtb(w, h, sex, cara, age):
    hh=h
    if cara=='Terlentang' and age>=24: hh=h-0.7
    elif cara=='Berdiri' and age<24: hh=h+0.7
    L,M,S=_ilms_h(hh, WFL_BOYS if sex=='L' else WFL_GIRLS)
    return lms_z(w,L,M,S)

def calc_tbu(h, age, sex):
    s3n,s2n,med,s2p,s3p=_ihfa(age, HFA_BOYS if sex=='L' else HFA_GIRLS)
    if h>=med:
        sd=(s2p-med)/2; z=(h-med)/sd if sd else 0
        if z>3: sd23=s3p-s2p; z=3+(h-s3p)/sd23 if sd23 else 3
    else:
        sd=(med-s2n)/2; z=(h-med)/sd if sd else 0
        if z<-3: sd23=s2n-s3n; z=-3-(s3n-h)/sd23 if sd23 else -3
    return round(z,2)

def get_median_tbu(age, sex):
    _,_,med,_,_=_ihfa(age, HFA_BOYS if sex=='L' else HFA_GIRLS)
    return round(med,1)

def get_median_bbu(age, sex):
    _,M,_=_ilms_age(age, WFA_BOYS if sex=='L' else WFA_GIRLS)
    return round(M,2)

# ══════════════════════════════════════════════
# LABEL HELPERS — KLASIFIKASI PERMENKES No.2/2020
# (identik dengan klasifikasi di notebook ipynb)
# ══════════════════════════════════════════════
def lbl_bbu(z):
    if z<-3: return "Sangat Kurang","#b91c1c","rgba(185,28,28,.1)"
    if z<-2: return "Kurang",       "#c2410c","rgba(194,65,12,.1)"
    if z<=1: return "Normal",       "#059669","rgba(5,150,105,.1)"
    return        "Risiko Lebih",   "#b45309","rgba(180,83,9,.1)"

def lbl_bbtb(z):
    if z<-3: return "Gizi Buruk",  "#b91c1c","rgba(185,28,28,.1)"
    if z<-2: return "Gizi Kurang", "#c2410c","rgba(194,65,12,.1)"
    if z<=1: return "Gizi Baik",   "#059669","rgba(5,150,105,.1)"
    if z<=2: return "Risiko Lebih","#b45309","rgba(180,83,9,.1)"
    if z<=3: return "Gizi Lebih",  "#92400e","rgba(146,64,14,.1)"
    return "Obesitas",             "#991b1b","rgba(153,27,27,.1)"

def lbl_tbu(z):
    if z<-3: return "Sangat Pendek","#b91c1c","rgba(185,28,28,.1)"
    if z<-2: return "Pendek",       "#c2410c","rgba(194,65,12,.1)"
    if z<=3: return "Normal",       "#059669","rgba(5,150,105,.1)"
    return "Tinggi",                "#0e7490","rgba(14,116,144,.1)"

# ══════════════════════════════════════════════
# OPSI DROPDOWN STATUS — SESUAI NILAI UNIK DATASET ASLI
# (Data-fix-gabungan.xlsx, kolom BB/U · TB/U · BB/TB)
# ══════════════════════════════════════════════
OPT_BBU  = ["Sangat Kurang","Kurang","Gizi Buruk","Gizi Kurang",
            "Normal","Gizi Baik","Risiko Lebih","Gizi Lebih"]
OPT_TBU  = ["Sangat Pendek","Pendek","Normal","Tinggi"]
OPT_BBTB = ["Sangat Kurus","Kurus","Gizi Kurang","Gizi Baik",
            "Normal","Risiko Gizi Lebih","Gizi Lebih","Obesitas"]

STATUS_COLOR = {
    "Sangat Kurang":("#b91c1c","rgba(185,28,28,.1)"),
    "Kurang":("#c2410c","rgba(194,65,12,.1)"),
    "Gizi Buruk":("#b91c1c","rgba(185,28,28,.1)"),
    "Gizi Kurang":("#c2410c","rgba(194,65,12,.1)"),
    "Sangat Kurus":("#b91c1c","rgba(185,28,28,.1)"),
    "Kurus":("#c2410c","rgba(194,65,12,.1)"),
    "Normal":("#059669","rgba(5,150,105,.1)"),
    "Gizi Baik":("#059669","rgba(5,150,105,.1)"),
    "Risiko Lebih":("#b45309","rgba(180,83,9,.1)"),
    "Risiko Gizi Lebih":("#b45309","rgba(180,83,9,.1)"),
    "Gizi Lebih":("#92400e","rgba(146,64,14,.1)"),
    "Obesitas":("#991b1b","rgba(153,27,27,.1)"),
    "Sangat Pendek":("#b91c1c","rgba(185,28,28,.1)"),
    "Pendek":("#c2410c","rgba(194,65,12,.1)"),
    "Tinggi":("#0e7490","rgba(14,116,144,.1)"),
}

def status_default_bbu(z):
    """Klasifikasi ZS BB/U → kosakata dataset asli (Permenkes)."""
    if z<-3: return "Sangat Kurang"
    if z<-2: return "Kurang"
    if z<=1: return "Normal"
    return "Risiko Lebih"

def status_default_tbu(z):
    if z<-3: return "Sangat Pendek"
    if z<-2: return "Pendek"
    if z<=3: return "Normal"
    return "Tinggi"

def status_default_bbtb(z):
    """Klasifikasi ZS BB/TB → kosakata dataset asli."""
    if z<-3: return "Sangat Kurus"
    if z<-2: return "Kurus"
    if z<=1: return "Gizi Baik"
    if z<=2: return "Risiko Gizi Lebih"
    if z<=3: return "Gizi Lebih"
    return "Obesitas"

def risk_tier(pct, thr):
    """Tier risiko relatif terhadap threshold optimal model (dari model.pkl).
    Prediksi 'Stunting' jika probabilitas >= threshold (sesuai notebook)."""
    lo  = max(0.0, thr - 15.0)
    hi  = min(95.0, thr + 20.0)
    if pct < lo:
        return dict(cls="rc-n",icon="✓",title="Tumbuh Kembang Normal",color="#059669",
                    eyebrow="STATUS PERTUMBUHAN · AMAN",
                    level="Rendah",priority="Rutin",pred="Tidak Stunting",
                    recs_immediate=["Pertahankan asupan gizi seimbang dan ASI/MPASI sesuai usia",
                                    "Pemantauan rutin di posyandu setiap bulan"],
                    recs_nutrition=["Konsumsi protein hewani: telur, ikan, daging, ayam",
                                    "Lengkapi dengan sayuran berwarna dan buah-buahan"],
                    recs_monitoring=["Timbang dan ukur tinggi badan setiap bulan",
                                     "Catat di buku KIA dan bandingkan dengan kurva WHO"])
    elif pct < thr:
        return dict(cls="rc-w",icon="○",title="Perlu Diwaspadai",color="#b45309",
                    eyebrow="STATUS PERTUMBUHAN · PERLU PERHATIAN",
                    level="Sedang-Rendah",priority="Segera",pred="Tidak Stunting",
                    recs_immediate=["Konsultasikan ke petugas gizi atau bidan untuk evaluasi",
                                    "Evaluasi kecukupan makan harian anak secara mendetail"],
                    recs_nutrition=["Tingkatkan asupan protein: 2–3 porsi/hari dari sumber hewani",
                                    "Pastikan asupan zat besi dan zinc terpenuhi dari makanan"],
                    recs_monitoring=["Pantau BB dan TB setiap bulan dengan cermat",
                                     "Catat pertumbuhan di grafik KMS dan waspadai plateau"])
    elif pct < hi:
        return dict(cls="rc-s",icon="⚡",title="Risiko Stunting Sedang",color="#c2410c",
                    eyebrow="PERHATIAN · INTERVENSI GIZI DIANJURKAN",
                    level="Sedang-Tinggi",priority="Mendesak",pred="Stunting",
                    recs_immediate=["Bawa ke dokter atau ahli gizi anak dalam waktu dekat",
                                    "Periksa kemungkinan penyakit infeksi berulang (ISPA, diare)"],
                    recs_nutrition=["Program PMT (Pemberian Makanan Tambahan) jika tersedia",
                                    "Pertimbangkan suplementasi: vitamin A, zinc, zat besi dosis terapeutik"],
                    recs_monitoring=["Pemantauan pertumbuhan setiap 2 minggu",
                                     "Foto dokumentasi untuk melacak perubahan visual kondisi anak"])
    else:
        return dict(cls="rc-t",icon="⚠️",title="Risiko Stunting Tinggi",color="#b91c1c",
                    eyebrow="PERHATIAN · TINDAK LANJUT SEGERA",
                    level="Tinggi",priority="Darurat",pred="Stunting",
                    recs_immediate=["Bawa ke puskesmas atau dokter spesialis anak SEGERA",
                                    "Lakukan pemeriksaan laboratorium: Hb, albumin, infeksi"],
                    recs_nutrition=["Intervensi gizi intensif terstruktur dengan pendampingan nakes",
                                    "F-75 / F-100 atau RUTF jika dinyatakan SAM oleh dokter"],
                    recs_monitoring=["Pemantauan pertumbuhan setiap minggu dengan tim medis",
                                     "Rawat inap mungkin diperlukan jika ada komplikasi"])

# ══════════════════════════════════════════════
# FEATURE ENGINEERING — IDENTIK DENGAN NOTEBOOK
# Prediksi_Stunting_Final_2.ipynb (Permenkes No.2/2020)
# ══════════════════════════════════════════════
def build_features(umur_bulan, jk, berat, tinggi, cara_ukur,
                   zs_bbu_manual=None, zs_bbtb_manual=None, rank_ref=None):
    # Z-score: dihitung dari tabel WHO 2006, atau pakai input manual jika ada
    zs_bb_u  = zs_bbu_manual  if zs_bbu_manual  is not None else calc_bbu(berat, umur_bulan, jk)
    zs_bb_tb = zs_bbtb_manual if zs_bbtb_manual is not None else calc_bbtb(berat, tinggi, jk, cara_ukur, umur_bulan)

    # 4a. Demografis (identik notebook)
    jk_enc   = 1 if jk=='L' else 0
    cara_enc = 1 if cara_ukur=='Berdiri' else 0

    # 4b. Kelompok usia Permenkes — pd.cut(bins=[-1,6,11,23,36,60], labels=[0..4])
    bins=[-1,6,11,23,36,60]; kel=0
    for i in range(len(bins)-1):
        if umur_bulan>bins[i] and umur_bulan<=bins[i+1]: kel=[0,1,2,3,4][i]
    fw=1 if umur_bulan<=23 else 0                 # f_window_1000hpk
    fm=1 if 6<=umur_bulan<=23 else 0              # f_masa_mpasi (between inclusive)
    fb=1 if umur_bulan<=23 else 0                 # f_baduta
    asq=umur_bulan**2; alg=np.log1p(umur_bulan)

    # 4c. Indeks BB/U
    bsk=1 if zs_bb_u<-3 else 0
    bk =1 if -3<=zs_bb_u<-2 else 0
    bn =1 if -2<=zs_bb_u<=1 else 0
    brl=1 if zs_bb_u>1 else 0
    uw =1 if zs_bb_u<-2 else 0

    # 4d. Indeks BB/TB
    gb =1 if zs_bb_tb<-3 else 0
    gk =1 if -3<=zs_bb_tb<-2 else 0
    gbk=1 if -2<=zs_bb_tb<=1 else 0
    rgl=1 if 1<zs_bb_tb<=2 else 0
    gl =1 if 2<zs_bb_tb<=3 else 0
    ob =1 if zs_bb_tb>3 else 0
    wst=1 if zs_bb_tb<-2 else 0

    # 4e. Zona borderline — notebook: mild = -2 <= zs < -1
    bm =1 if -2<=zs_bb_u<-1 else 0
    btm=1 if -2<=zs_bb_tb<-1 else 0
    pb2 =max(0, -2-zs_bb_u);  ptb2=max(0, -2-zs_bb_tb)
    pb3 =max(0, -3-zs_bb_u);  ptb3=max(0, -3-zs_bb_tb)

    # 4f. Komposit — RUMUS PERSIS NOTEBOOK
    fdbl=1 if (uw==1 and wst==1) else 0
    fds =1 if (bsk==1 and gb==1) else 0
    fas =1 if (bsk==1 or gb==1) else 0
    sk = (bk*1 + bsk*2 + gk*1 + gb*2 + bm*0.5 + btm*0.5 + fm*0.5)
    ji = min(2, uw + wst)

    # 4g. Kombinasi z-score — harmonic dengan +1e-8 persis notebook
    az =(zs_bb_u+zs_bb_tb)/2
    mnz=min(zs_bb_u,zs_bb_tb); mxz=max(zs_bb_u,zs_bb_tb)
    gp =zs_bb_u-zs_bb_tb; abg=abs(gp); pr=zs_bb_u*zs_bb_tb
    hm =(2*zs_bb_u*zs_bb_tb)/(zs_bb_u+zs_bb_tb+1e-8)
    bs2=zs_bb_u**2; bts2=zs_bb_tb**2; bs3=zs_bb_u**3; bts3=zs_bb_tb**3

    # 4h. Interaksi
    uxr=umur_bulan*sk; uxm=umur_bulan*mnz
    uxb=umur_bulan*zs_bb_u; uxt=umur_bulan*zs_bb_tb
    bxw=fb*wst; mxu=fm*uw
    jxm=jk_enc*mnz; jxb=jk_enc*zs_bb_u; jxr=jk_enc*sk

    # 4i. Antropometri langsung — pembagi (umur+1) persis notebook
    bmi=berat/((tinggi/100)**2)
    rbt=berat/tinggi
    rtu=tinggi/(umur_bulan+1)
    rbu=berat/(umur_bulan+1)

    # 4j. Rank percentile — pakai distribusi z-score data training jika
    # tersedia di model.pkl ("rank_ref"); jika tidak, aproksimasi sigmoid
    if rank_ref is not None:
        ref_bbu  = np.asarray(rank_ref.get("zs_bb_u", []))
        ref_bbtb = np.asarray(rank_ref.get("zs_bb_tb", []))
        rb   = float(np.searchsorted(np.sort(ref_bbu),  zs_bb_u,  side="right")/len(ref_bbu))  if len(ref_bbu)  else float(1/(1+np.exp(-zs_bb_u)))
        rbt2 = float(np.searchsorted(np.sort(ref_bbtb), zs_bb_tb, side="right")/len(ref_bbtb)) if len(ref_bbtb) else float(1/(1+np.exp(-zs_bb_tb)))
    else:
        rb  =float(1/(1+np.exp(-zs_bb_u)))
        rbt2=float(1/(1+np.exp(-zs_bb_tb)))

    row={
        'umur_bulan':umur_bulan,'jk_encoded':jk_enc,'cara_ukur_encoded':cara_enc,
        'kel_usia_permenkes':float(kel),'f_window_1000hpk':fw,'f_masa_mpasi':fm,
        'f_baduta':fb,'age_sq':asq,'age_log':alg,'zs_bb_u':zs_bb_u,
        'f_bb_sangat_kurang':bsk,'f_bb_kurang':bk,'f_bb_normal':bn,'f_bb_risiko_lebih':brl,
        'f_underweight':uw,'zs_bb_tb':zs_bb_tb,'f_gizi_buruk':gb,'f_gizi_kurang':gk,
        'f_gizi_baik':gbk,'f_risiko_gizi_lebih':rgl,'f_gizi_lebih':gl,'f_obesitas':ob,
        'f_wasting':wst,'f_bb_mild':bm,'f_bbtb_mild':btm,
        'prox_bbu_ke_minus2':pb2,'prox_bbtb_ke_minus2':ptb2,'prox_bbu_ke_minus3':pb3,
        'prox_bbtb_ke_minus3':ptb3,'f_double_malnutrisi':fdbl,'f_double_severe':fds,
        'f_any_severe':fas,'skor_risiko_gizi':sk,'jml_indeks_masalah':ji,
        'avg_zs_bbu_bbtb':az,'min_zs_bbu_bbtb':mnz,'max_zs_bbu_bbtb':mxz,
        'gap_bbu_bbtb':gp,'abs_gap_bbu_bbtb':abg,'product_zs':pr,'harmonic_zs':hm,
        'zs_bbu_sq':bs2,'zs_bbtb_sq':bts2,'zs_bbu_cb':bs3,'zs_bbtb_cb':bts3,
        'umur_x_risiko':uxr,'umur_x_minzs':uxm,'umur_x_bbu':uxb,'umur_x_bbtb':uxt,
        'baduta_x_wasting':bxw,'mpasi_x_underw':mxu,'jk_x_minzs':jxm,'jk_x_bbu':jxb,
        'jk_x_risiko':jxr,'bmi_proxy':bmi,'rasio_bb_tb':rbt,'rasio_tb_umur':rtu,
        'rasio_bb_umur':rbu,'berat':berat,'tinggi':tinggi,'rank_bbu':rb,'rank_bbtb':rbt2
    }
    feats=['umur_bulan','jk_encoded','cara_ukur_encoded','kel_usia_permenkes',
           'f_window_1000hpk','f_masa_mpasi','f_baduta','age_sq','age_log','zs_bb_u',
           'f_bb_sangat_kurang','f_bb_kurang','f_bb_normal','f_bb_risiko_lebih','f_underweight',
           'zs_bb_tb','f_gizi_buruk','f_gizi_kurang','f_gizi_baik','f_risiko_gizi_lebih',
           'f_gizi_lebih','f_obesitas','f_wasting','f_bb_mild','f_bbtb_mild',
           'prox_bbu_ke_minus2','prox_bbtb_ke_minus2','prox_bbu_ke_minus3','prox_bbtb_ke_minus3',
           'f_double_malnutrisi','f_double_severe','f_any_severe','skor_risiko_gizi',
           'jml_indeks_masalah','avg_zs_bbu_bbtb','min_zs_bbu_bbtb','max_zs_bbu_bbtb',
           'gap_bbu_bbtb','abs_gap_bbu_bbtb','product_zs','harmonic_zs',
           'zs_bbu_sq','zs_bbtb_sq','zs_bbu_cb','zs_bbtb_cb',
           'umur_x_risiko','umur_x_minzs','umur_x_bbu','umur_x_bbtb',
           'baduta_x_wasting','mpasi_x_underw','jk_x_minzs','jk_x_bbu','jk_x_risiko',
           'bmi_proxy','rasio_bb_tb','rasio_tb_umur','rasio_bb_umur','berat','tinggi',
           'rank_bbu','rank_bbtb']
    df=pd.DataFrame([row])[feats]
    return df.replace([np.inf,-np.inf],np.nan).fillna(0), zs_bb_u, zs_bb_tb

# ══════════════════════════════════════════════
# MODEL — model.pkl dari notebook:
# {"model": XGBClassifier, "threshold": 0.579, "features": [...]}
# ══════════════════════════════════════════════
class XGBoostModel:  # kompatibilitas jika pkl lama berisi ensemble custom
    def __init__(self, models, weights=None):
        self.models=models; self.weights=weights if weights else [1/len(models)]*len(models)
    def predict_proba(self, X):
        p=np.zeros((X.shape[0],2))
        for m,w in zip(self.models,self.weights): p+=w*m.predict_proba(X)
        return p

@st.cache_resource
def load_model():
    import sys,types
    mod=types.ModuleType("__main__"); mod.XGBoost=XGBoostModel; mod.XGBoostModel=XGBoostModel
    sys.modules["__main__"]=mod
    data=joblib.load("model.pkl")
    rank_ref=None; feat_order=None
    if isinstance(data,dict):
        model=data["model"]
        threshold=float(data.get("threshold",0.579))   # default = threshold notebook
        feat_order=data.get("features")
        rank_ref=data.get("rank_ref")                  # opsional (lihat catatan)
    else:
        model=data; threshold=0.579
    return model,threshold,feat_order,rank_ref

def predict(umur,jk,berat,tinggi,cara, zs_bbu_manual=None, zs_bbtb_manual=None):
    model,thr,feat_order,rank_ref=load_model()
    X,zb,zbt=build_features(umur,jk,berat,tinggi,cara,
                            zs_bbu_manual=zs_bbu_manual,
                            zs_bbtb_manual=zs_bbtb_manual,
                            rank_ref=rank_ref)
    if feat_order:                       # pastikan urutan kolom = urutan training
        X=X[feat_order]
    p=model.predict_proba(X)[0]
    return p[1]*100, max(p)*100, zb, zbt, thr*100

# ══════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════
def validate(umur, berat, tinggi):
    warns=[]
    bmin_m={0:2.0,6:5.5,12:7.0,24:9.0,36:11.0,48:13.0,60:15.0}
    bmax_m={0:5.5,6:10.5,12:14.0,24:17.0,36:20.0,48:23.0,60:27.0}
    bmin=bmax=None
    for k in sorted(bmin_m):
        if umur>=k: bmin,bmax=bmin_m[k],bmax_m[k]
    if bmin and berat<bmin: warns.append(f"BB {berat} kg terlalu rendah untuk usia {umur} bln (min ≈{bmin} kg)")
    if bmax and berat>bmax: warns.append(f"BB {berat} kg terlalu tinggi untuk usia {umur} bln (maks ≈{bmax} kg)")
    tmin_m={0:44,6:60,12:68,24:78,36:86,48:93,60:100}
    tmax_m={0:57,6:74,12:84,24:97,36:107,48:116,60:123}
    tmin=tmax=None
    for k in sorted(tmin_m):
        if umur>=k: tmin,tmax=tmin_m[k],tmax_m[k]
    if tmin and tinggi<tmin: warns.append(f"TB {tinggi} cm tidak realistis untuk usia {umur} bln (min ≈{tmin} cm)")
    if tmax and tinggi>tmax: warns.append(f"TB {tinggi} cm tidak realistis untuk usia {umur} bln (maks ≈{tmax} cm)")
    return warns

# ══════════════════════════════════════════════
# FUTURE PROJECTION
# ══════════════════════════════════════════════
def project_future(umur, jk, berat, tinggi, cara, months_ahead=6):
    model, thr, feat_order, rank_ref = load_model()
    results = []
    weight_velocity = {0:0.90, 3:0.65, 6:0.40, 9:0.32, 12:0.22, 18:0.18, 24:0.14, 36:0.12, 48:0.10}
    height_velocity = {0:3.5,  3:2.5,  6:1.8,  9:1.4,  12:1.1,  18:1.0,  24:0.9,  36:0.8,  48:0.7}

    def get_vel(d, age):
        keys = sorted(d.keys())
        for k in reversed(keys):
            if age >= k: return d[k]
        return list(d.values())[-1]

    cur_b, cur_t, cur_u = berat, tinggi, umur
    for m in range(1, months_ahead+1):
        wv = get_vel(weight_velocity, cur_u)
        hv = get_vel(height_velocity, cur_u)
        cur_b = round(cur_b + wv, 2)
        cur_t = round(cur_t + hv, 1)
        cur_u = min(60, umur + m)
        try:
            X, zb, zbt = build_features(cur_u, jk, cur_b, cur_t, cara, rank_ref=rank_ref)
            if feat_order: X = X[feat_order]
            prob = model.predict_proba(X)[0][1] * 100
            zt   = calc_tbu(cur_t, cur_u, jk)
            tc, tcol, _ = lbl_tbu(zt)
        except:
            prob, zt, tc, tcol = 0, 0, "—", "#64748b"
        results.append({
            "bulan_ke": m, "umur": cur_u, "bb": cur_b, "tb": cur_t,
            "zs_tbu": zt, "status_tb": tc, "tcol": tcol, "prob": prob,
        })
    return results

# ══════════════════════════════════════════════
# PLOT — FUTURE PROB TREND
# ══════════════════════════════════════════════
def plot_future(base_pct, rows, tier_color, thr_pct):
    months = [0] + [r["bulan_ke"] for r in rows]
    probs  = [base_pct] + [r["prob"] for r in rows]

    fig, ax = plt.subplots(figsize=(9,3.6))
    fig.patch.set_facecolor("#ffffff"); ax.set_facecolor("#f8faff")

    fill_color = "#059669" if base_pct<thr_pct else "#b91c1c"
    ax.fill_between(months, probs, alpha=.1, color=fill_color)
    ax.plot(months, probs, "-o", color=tier_color, lw=2.5, markersize=8,
            zorder=3, markerfacecolor="#ffffff", markeredgewidth=2.5)
    ax.axhline(thr_pct, color="#b45309", lw=1.2, linestyle="--", alpha=.7,
               label=f"Threshold model {thr_pct:.1f}%")
    ax.axhspan(0, thr_pct, alpha=.04, color="#059669")
    ax.axhspan(thr_pct, 100, alpha=.04, color="#b91c1c")

    if rows:
        ax.annotate(f"{probs[-1]:.1f}%", (months[-1], probs[-1]),
                    textcoords="offset points", xytext=(8, 4),
                    color=tier_color, fontsize=9.5, fontweight='700')

    ax.set_ylim(0, 100); ax.set_xlim(-0.2, len(months)-0.7)
    ax.set_xlabel("Bulan ke depan", color="#475569", fontsize=8.5)
    ax.set_ylabel("Probabilitas Stunting (%)", color="#475569", fontsize=8.5)
    ax.set_title("Proyeksi Probabilitas Stunting — Pertumbuhan Median WHO",
                 color="#0d1f5c", fontsize=9.5, fontweight='600', pad=10)
    ax.tick_params(colors="#64748b", labelsize=8)
    for sp in ['bottom','left']: ax.spines[sp].set_color("#bfdbfe")
    for sp in ['top','right']:   ax.spines[sp].set_visible(False)
    ax.grid(color="#dbeafe", linestyle="--", linewidth=0.7, alpha=.9)
    ax.legend(fontsize=8.5, facecolor="#ffffff", edgecolor="#dbeafe", labelcolor="#475569",
              framealpha=.95)
    plt.tight_layout(pad=2)
    return fig

# ══════════════════════════════════════════════
# ABOUT MODEL — METRIC CHART
# ══════════════════════════════════════════════
MODEL_METRICS = {"Accuracy":0.969,"Precision":0.903,"Recall":0.933,"F1-Score":0.918,"AUC-ROC":0.991}
FEAT_IMP = [
    ("Z-Score BB/TB",18.4),("Z-Score BB/U",14.2),("Tinggi Badan",11.7),
    ("Min Z-Score",8.9),("Umur × Z-Min",7.3),("Berat Badan",6.8),
    ("Skor Risiko Gizi",5.9),("Umur",5.4),("Rasio BB/TB",4.1),("BMI Proxy",3.8),
    ("Prox −2SD BB/TB",3.2),("Prox −2SD BB/U",2.8),
]

def plot_metrics():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    fig.patch.set_facecolor("#ffffff")

    ax = axes[0]; ax.set_facecolor("#f8faff")
    lbs = list(MODEL_METRICS.keys()); vals = [v*100 for v in MODEL_METRICS.values()]
    cols = ["#0d1f5c","#1a3480","#1e4db7","#2563eb","#60a5fa"]
    bars = ax.bar(lbs, vals, color=cols, width=0.52, edgecolor="none", zorder=3)
    for b,v in zip(bars,vals):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, f"{v:.1f}%",
                ha='center',va='bottom',color="#0d1f5c",fontsize=8.5,fontweight='700')
    ax.set_ylim(82,100); ax.set_title("Performa Model pada Test Set (20%)",
                                       color="#0d1f5c",fontsize=9.5,fontweight='600',pad=10)
    ax.tick_params(colors="#64748b",labelsize=8.5)
    for sp in ['bottom','left']: ax.spines[sp].set_color("#bfdbfe")
    for sp in ['top','right']:   ax.spines[sp].set_visible(False)
    ax.grid(axis='y',color="#dbeafe",linestyle="--",linewidth=0.7,alpha=1,zorder=0)

    ax2 = axes[1]; ax2.set_facecolor("#f8faff")
    names=[f[0] for f in FEAT_IMP[:10]][::-1]
    fvals=[f[1] for f in FEAT_IMP[:10]][::-1]
    fcols=["#0d1f5c" if v>=12 else ("#1e4db7" if v>=7 else "#93c5fd") for v in fvals]
    bars2 = ax2.barh(names, fvals, color=fcols, height=0.58, edgecolor="none", zorder=3)
    for i,(n,v) in enumerate(zip(names,fvals)):
        ax2.text(v+0.15, i, f"{v:.1f}%", va='center', ha='left',
                 color="#0d1f5c", fontsize=7.5, fontweight='600')
    ax2.set_xlabel("Kontribusi (%)", color="#475569", fontsize=8)
    ax2.set_title("Feature Importance", color="#0d1f5c", fontsize=9.5, fontweight='600', pad=10)
    ax2.tick_params(colors="#64748b", labelsize=8)
    for sp in ['bottom','left']: ax2.spines[sp].set_color("#bfdbfe")
    for sp in ['top','right']:   ax2.spines[sp].set_visible(False)
    ax2.grid(axis='x',color="#dbeafe",linestyle="--",linewidth=0.7,alpha=1,zorder=0)
    ax2.set_xlim(0, max(fvals)+4)

    plt.tight_layout(pad=2)
    return fig

# ══════════════════════════════════════════════
# ══  RENDER  ══════════════════════════════════
# ══════════════════════════════════════════════

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── DECORATIVE FLOATING SHAPES ─────────────────
st.markdown("""
<div style="position:relative;pointer-events:none;height:0;overflow:visible;z-index:0;margin-bottom:-1rem;">
    <svg style="position:absolute;top:-30px;right:-40px;width:280px;height:280px;" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="190" cy="115" r="105" stroke="#2563eb" stroke-width="1" stroke-dasharray="6 10" opacity=".18"/>
        <circle cx="190" cy="115" r="74" stroke="#60a5fa" stroke-width="0.7" stroke-dasharray="4 14" opacity=".14"/>
        <circle cx="100" cy="44" r="5" fill="#bfdbfe" opacity=".65"/>
        <circle cx="258" cy="70" r="3.5" fill="#93c5fd" opacity=".55"/>
        <circle cx="240" cy="195" r="5.5" fill="#dbeafe" opacity=".7"/>
        <circle cx="130" cy="210" r="3" fill="#60a5fa" opacity=".45"/>
        <circle cx="215" cy="36" r="2.5" fill="#3b82f6" opacity=".4"/>
        <circle cx="226" cy="36" r="2.5" fill="#3b82f6" opacity=".4"/>
        <circle cx="220" cy="29" r="2.5" fill="#3b82f6" opacity=".4"/>
        <circle cx="220" cy="43" r="2.5" fill="#3b82f6" opacity=".4"/>
        <polygon points="268,158 250,188 286,188" stroke="#93c5fd" stroke-width="0.9" fill="none" opacity=".3"/>
        <rect x="58" y="150" width="11" height="11" rx="2" stroke="#3b82f6" stroke-width="0.8" fill="none" opacity=".25"/>
    </svg>
    <svg style="position:absolute;top:200px;left:-50px;width:200px;height:200px;" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <polygon points="100,15 165,52 165,128 100,165 35,128 35,52" stroke="#2563eb" stroke-width="0.8" stroke-dasharray="5 9" fill="none" opacity=".2"/>
        <polygon points="100,35 148,62 148,118 100,145 52,118 52,62" stroke="#60a5fa" stroke-width="0.6" stroke-dasharray="3 12" fill="none" opacity=".15"/>
        <circle cx="30" cy="32" r="4" fill="#bfdbfe" opacity=".65"/>
        <circle cx="170" cy="168" r="3.5" fill="#93c5fd" opacity=".55"/>
        <circle cx="42" cy="158" r="5" fill="#dbeafe" opacity=".7"/>
        <rect x="154" y="22" width="10" height="10" rx="2" stroke="#3b82f6" stroke-width="0.7" fill="none" opacity=".25"/>
        <rect x="159" y="27" width="10" height="10" rx="2" stroke="#60a5fa" stroke-width="0.5" fill="none" opacity=".16"/>
    </svg>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-inner">
        <div class="hero-pill">
            <div class="hero-pill-dot"></div>
            Sistem Prediksi Data Science &nbsp;·&nbsp; Permenkes No. 2 Tahun 2020
        </div>
        <h1 class="hero-title">Prediksi <em>Stunting</em> Balita</h1>
        <div class="hero-divider"></div>
        <p class="hero-sub">
            Analisis antropometri berbasis WHO 2006 Growth Standards
            &nbsp;·&nbsp; CatBoost &amp; XGBoost &nbsp;·&nbsp; 61 Variabel Feature Engineering
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────
tab_pred, tab_future, tab_about = st.tabs([
    "🔍  Prediksi & Analisis",
    "📈  Proyeksi Masa Depan",
    "📚  Tentang Model",
])

# ══════════════════════════════════════════════
# TAB 1 — PREDIKSI
# ══════════════════════════════════════════════
with tab_pred:
    st.markdown('<p class="slabel">Data Antropometri Anak</p>', unsafe_allow_html=True)

    # ── INPUT: identitas & tanggal
    c1, c2, c3 = st.columns(3)
    with c1:
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki","Perempuan"], key="p_jk")
    with c2:
        tgl_lahir = st.date_input("Tanggal Lahir",
                                  value=date.today() - relativedelta(months=24),
                                  min_value=date(2019, 1, 1),
                                  max_value=date.today(),
                                  format="DD/MM/YYYY", key="p_lahir")
    with c3:
        tgl_ukur = st.date_input("Tanggal Pengukuran",
                                 value=date.today(),
                                 min_value=date(2019, 1, 1),
                                 max_value=date.today(),
                                 format="DD/MM/YYYY", key="p_ukur")

    # ── UMUR: bisa otomatis dari tanggal, bisa diketik manual
    umur_auto = hitung_umur_bulan(tgl_lahir, tgl_ukur)
    if umur_auto is None:
        st.error("Tanggal pengukuran tidak boleh sebelum tanggal lahir.")
        st.stop()

    cu1, cu2 = st.columns([1.3, 2])
    with cu1:
        auto_umur = st.checkbox("Hitung umur otomatis dari tanggal",
                                value=True, key="p_auto_umur",
                                help="Centang: umur dihitung dari Tanggal Lahir → Tanggal Pengukuran (umur penuh). Hilangkan centang untuk mengetik umur sendiri.")
    if auto_umur:
        umur_bulan = umur_auto
        with cu2:
            umur_valid = 0 <= umur_bulan <= 60
            u_col = "#1e4db7" if umur_valid else "#b91c1c"
            st.markdown(f"""
            <div style="background:#ffffff;border:1.5px solid var(--b100);border-left:4px solid {u_col};
                        border-radius:var(--r-md);padding:.7rem 1.2rem;
                        box-shadow:var(--shadow-sm);display:flex;align-items:baseline;gap:.8rem;">
                <span style="font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;color:#94a3b8;font-weight:700;">Umur (Bulan)</span>
                <span style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:{u_col};line-height:1;">{umur_bulan}</span>
                <span style="font-size:.7rem;color:#94a3b8;">bulan penuh (otomatis)</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        with cu2:
            umur_bulan = st.number_input("Umur (Bulan) — input manual", 0, 60,
                                         int(min(60, max(0, umur_auto))), 1, key="p_umur_manual")
        umur_valid = True
    if not (0 <= umur_bulan <= 60):
        umur_valid = False
        st.warning("⚠️ Umur di luar rentang 0–60 bulan. Model hanya valid untuk balita 0–60 bulan (Permenkes No.2/2020).")
    else:
        umur_valid = True

    # ── INPUT: antropometri
    c4, c5 = st.columns(2)
    with c4:
        berat  = st.number_input("Berat Badan (kg)", 1.0, 35.0, 12.0, 0.1, format="%.1f", key="p_bb")
    with c5:
        tinggi = st.number_input("Tinggi / Panjang Badan (cm)", 40.0, 130.0, 87.0, 0.1, format="%.1f", key="p_tb")

    # Cara ukur — default mengikuti usia sesuai Permenkes
    cara_default = 1 if umur_bulan >= 24 else 0
    cara_ukur = st.selectbox("Cara Pengukuran",
                             ["Terlentang — Panjang Badan", "Berdiri — Tinggi Badan"],
                             index=cara_default, key="p_cara",
                             help="Permenkes: usia < 24 bln diukur Terlentang · usia ≥ 24 bln diukur Berdiri")

    cu_mode = "Berdiri" if cara_ukur.startswith("Berdiri") else "Terlentang"
    jk      = "L" if jenis_kelamin == "Laki-laki" else "P"

    if umur_bulan < 24 and cu_mode == "Berdiri":
        st.warning("⚠️ Usia < 24 bulan: disarankan pengukuran Terlentang.")
    elif umur_bulan >= 24 and cu_mode == "Terlentang":
        st.warning("⚠️ Usia ≥ 24 bulan: disarankan pengukuran Berdiri.")
    for w in validate(umur_bulan, berat, tinggi):
        st.warning(f"⚠️ {w}")

    # ══════════════════════════════════════════
    # INDEKS ANTROPOMETRI: BB/U · TB/U · BB/TB
    # Z-Score DIISI MANUAL (kotak kosong sampai diketik)
    # Status: dropdown dengan kategori persis seperti dataset asli
    # ══════════════════════════════════════════
    st.markdown('<p class="slabel" style="margin-top:1.2rem;">Indeks Antropometri (Permenkes No.2/2020)</p>',
                unsafe_allow_html=True)

    z1, z2, z3 = st.columns(3)
    with z1:
        zs_bbu_in  = st.number_input("ZS BB/U", min_value=-10.0, max_value=10.0,
                                     value=None, step=0.01, format="%.2f",
                                     placeholder="Mis. -1.26", key="p_zs_bbu")
    with z2:
        zs_tbu_in  = st.number_input("ZS TB/U", min_value=-10.0, max_value=10.0,
                                     value=None, step=0.01, format="%.2f",
                                     placeholder="Mis. -0.41", key="p_zs_tbu")
    with z3:
        zs_bbtb_in = st.number_input("ZS BB/TB", min_value=-10.0, max_value=10.0,
                                     value=None, step=0.01, format="%.2f",
                                     placeholder="Mis. -1.66", key="p_zs_bbtb")
    st.caption("✏️ Ketik nilai Z-Score secara manual (mis. dari e-PPGBM / buku KIA / dataset). "
               "Catatan: data dengan ZS ≤ −10 dibuang saat training, sesuai notebook.")

    # ── STATUS DROPDOWN — kategori persis dataset asli (Data-fix-gabungan.xlsx)
    s1, s2, s3 = st.columns(3)
    with s1:
        st_bbu  = st.selectbox("BB/U (Status)", OPT_BBU, index=None,
                               placeholder="Pilih status…", key="p_st_bbu")
        if zs_bbu_in is not None:
            st.caption(f"Saran (Permenkes): **{status_default_bbu(zs_bbu_in)}**")
    with s2:
        st_tbu  = st.selectbox("TB/U (Status)", OPT_TBU, index=None,
                               placeholder="Pilih status…", key="p_st_tbu")
        if zs_tbu_in is not None:
            st.caption(f"Saran (Permenkes): **{status_default_tbu(zs_tbu_in)}**")
    with s3:
        st_bbtb = st.selectbox("BB/TB (Status)", OPT_BBTB, index=None,
                               placeholder="Pilih status…", key="p_st_bbtb")
        if zs_bbtb_in is not None:
            st.caption(f"Saran (Permenkes): **{status_default_bbtb(zs_bbtb_in)}**")

    # ── PRATINJAU KARTU INDEKS — kosong sebelum diisi, terisi setelah input
    def _card_vals(zs, status):
        if zs is None:
            return "—", "#cbd5e1", ("Belum diisi", "#94a3b8", "rgba(148,163,184,.12)")
        lbl = status if status else "—"
        col, bg = STATUS_COLOR.get(status, ("#94a3b8","rgba(148,163,184,.12)")) if status else ("#94a3b8","rgba(148,163,184,.12)")
        zcol = col if status else "#475569"
        return f"{zs:+.2f}", zcol, (lbl, col, bg)

    v1, vc1, (b1, bc1, bb1) = _card_vals(zs_bbu_in,  st_bbu)
    v2, vc2, (b2, bc2, bb2) = _card_vals(zs_tbu_in,  st_tbu)
    v3, vc3, (b3, bc3, bb3) = _card_vals(zs_bbtb_in, st_bbtb)
    tbu_warn = (zs_tbu_in is not None and zs_tbu_in < -2)
    st.markdown(f"""
    <div class="zrow" style="margin-top:.6rem;">
        <div class="zcard">
            <div class="ztag">BB/U &nbsp;·&nbsp; ZS BB/U</div>
            <div class="zval" style="color:{vc1};">{v1}</div>
            <div class="zdesc">Berat Badan menurut Umur</div>
            <span class="zbadge" style="background:{bb1};color:{bc1};">{b1}</span>
        </div>
        <div class="zcard" style="{'border-color:rgba(185,28,28,.3);' if tbu_warn else ''}">
            <div class="ztag">TB/U &nbsp;·&nbsp; ZS TB/U ★</div>
            <div class="zval" style="color:{vc2};">{v2}</div>
            <div class="zdesc">Tinggi Badan menurut Umur — Indikator Stunting</div>
            <span class="zbadge" style="background:{bb2};color:{bc2};">{b2}</span>
        </div>
        <div class="zcard">
            <div class="ztag">BB/TB &nbsp;·&nbsp; ZS BB/TB</div>
            <div class="zval" style="color:{vc3};">{v3}</div>
            <div class="zdesc">Berat Badan menurut Tinggi Badan — Wasting</div>
            <span class="zbadge" style="background:{bb3};color:{bc3};">{b3}</span>
        </div>
    </div>
    <div style="font-size:.66rem;color:#94a3b8;text-align:right;margin:-0.2rem 0 1rem;">
        ★ TB/U adalah target model (label stunting). Prediksi dihitung dari <b>nilai Z-Score</b> BB/U &amp; BB/TB
        (status dropdown hanya tampilan/pencatatan) — sesuai notebook, anti data-leakage.
    </div>
    """, unsafe_allow_html=True)

    zs_lengkap = (zs_bbu_in is not None) and (zs_tbu_in is not None) and (zs_bbtb_in is not None)
    if not zs_lengkap:
        st.info("ℹ️ Isi ketiga nilai Z-Score (ZS BB/U, ZS TB/U, ZS BB/TB) terlebih dahulu untuk mengaktifkan tombol prediksi.")

    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    btn = st.button("🔍  Analisis & Prediksi Sekarang", key="btn_pred",
                    disabled=(not umur_valid) or (not zs_lengkap))

    if btn:
        # status yang dipakai di hasil: pilihan pengguna, atau klasifikasi Permenkes jika belum dipilih
        st_bbu  = st_bbu  or status_default_bbu(zs_bbu_in)
        st_tbu  = st_tbu  or status_default_tbu(zs_tbu_in)
        st_bbtb = st_bbtb or status_default_bbtb(zs_bbtb_in)
        with st.spinner("Menganalisis data antropometri..."):
            try:
                pct, conf, zs_bbu, zs_bbtb, thr_pct = predict(
                    umur_bulan, jk, berat, tinggi, cu_mode,
                    zs_bbu_manual=float(zs_bbu_in),
                    zs_bbtb_manual=float(zs_bbtb_in))
                zs_tbu = float(zs_tbu_in)
                med_tb = get_median_tbu(umur_bulan, jk)
                med_bb = get_median_bbu(umur_bulan, jk)
            except Exception as e:
                st.error(f"Error: {e}"); st.stop()

        st.session_state["last"] = dict(umur=umur_bulan, jk=jk, berat=berat,
                                         tinggi=tinggi, cara=cu_mode, pct=pct,
                                         conf=conf, zs_bbu=zs_bbu, zs_bbtb=zs_bbtb,
                                         zs_tbu=zs_tbu, thr=thr_pct,
                                         tgl_lahir=str(tgl_lahir), tgl_ukur=str(tgl_ukur))
        tier = risk_tier(pct, thr_pct)

        st.markdown('<p class="slabel" style="margin-top:1.4rem;">Hasil Analisis</p>',
                    unsafe_allow_html=True)

        # ── STATUS CARD
        bar_pos = max(2, min(97, pct))
        st.markdown(f"""
        <div class="rcard {tier['cls']}">
            <div class="rc-eye" style="color:{tier['color']};">{tier['eyebrow']}</div>
            <div class="rc-ico">{tier['icon']}</div>
            <div class="rc-ttl" style="color:{tier['color']};">{tier['title']}</div>
            <div class="rc-sub">Prediksi model: <strong style="color:{tier['color']};">{tier['pred']}</strong>
                &nbsp;·&nbsp; Probabilitas stunting
                <strong style="color:{tier['color']};font-size:1.05rem;">{pct:.1f}%</strong>
                &nbsp;(threshold {thr_pct:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── CONFIDENCE + GAUGE
        ca, cb = st.columns([1, 2])
        conf_col = "#059669" if conf>=80 else ("#b45309" if conf>=60 else "#c2410c")
        conf_lbl = "Tinggi" if conf>=80 else ("Sedang" if conf>=60 else "Rendah")
        with ca:
            st.markdown(f"""
            <div class="conf-wrap">
                <div class="conf-ring" style="--rc:{conf_col};--pct:{conf:.0f}%;">
                    <span style="color:{conf_col};">{conf:.0f}%</span>
                </div>
                <div class="conf-info">
                    <div class="conf-lbl">Kepercayaan Model</div>
                    <div class="conf-val" style="color:{conf_col};">{conf_lbl}</div>
                    <div class="conf-desc">Keyakinan prediksi AI</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with cb:
            st.markdown(f"""
            <div class="gauge">
                <div class="gtop">
                    <span class="gttl">Probabilitas Stunting</span>
                    <span class="gnum" style="color:{tier['color']};">{pct:.1f}<span style="font-size:.8rem;opacity:.45;">%</span></span>
                </div>
                <div class="gtrack">
                    <div class="gfill"></div>
                    <div class="gpip" style="left:{bar_pos}%;color:{tier['color']};background:{tier['color']};"></div>
                </div>
                <div class="gtick"><span>Tidak Stunting</span><span>Threshold {thr_pct:.1f}%</span><span>Stunting</span></div>
            </div>
            """, unsafe_allow_html=True)

        # ── Z-SCORE CARDS (BB/U · TB/U · BB/TB) — nilai & status sesuai input
        bcol, bbg     = STATUS_COLOR.get(st_bbu,  ("#475569","rgba(71,85,105,.1)"))
        tcol, tbg     = STATUS_COLOR.get(st_tbu,  ("#475569","rgba(71,85,105,.1)"))
        btbcol, btbbg = STATUS_COLOR.get(st_bbtb, ("#475569","rgba(71,85,105,.1)"))
        st.markdown(f"""
        <div class="zrow">
            <div class="zcard">
                <div class="ztag">BB/U &nbsp;·&nbsp; ZS BB/U</div>
                <div class="zval" style="color:{bcol};">{zs_bbu:+.2f}</div>
                <div class="zdesc">Berat Badan menurut Umur</div>
                <span class="zbadge" style="background:{bbg};color:{bcol};">{st_bbu}</span>
            </div>
            <div class="zcard" style="{'border-color:rgba(185,28,28,.3);' if zs_tbu<-2 else ''}">
                <div class="ztag">TB/U &nbsp;·&nbsp; ZS TB/U ★</div>
                <div class="zval" style="color:{tcol};">{zs_tbu:+.2f}</div>
                <div class="zdesc">Indikator Stunting Utama</div>
                <span class="zbadge" style="background:{tbg};color:{tcol};">{st_tbu}</span>
            </div>
            <div class="zcard">
                <div class="ztag">BB/TB &nbsp;·&nbsp; ZS BB/TB</div>
                <div class="zval" style="color:{btbcol};">{zs_bbtb:+.2f}</div>
                <div class="zdesc">Wasting / Status Gizi</div>
                <span class="zbadge" style="background:{btbbg};color:{btbcol};">{st_bbtb}</span>
            </div>
        </div>
        <div style="font-size:.66rem;color:#94a3b8;text-align:right;margin:-0.2rem 0 1rem;">
            ★ TB/U = indikator stunting per WHO &amp; Permenkes No.2/2020
        </div>
        """, unsafe_allow_html=True)

        # ── INFO BAND
        selisih_tb = tinggi - med_tb
        sel_col_tb = "#059669" if selisih_tb >= 0 else "#c2410c"
        bmi_v = berat/(tinggi/100)**2
        kel_map = {0:"ASI Eksklusif",1:"MPASI Awal",2:"Baduta / 1000 HPK",3:"Batita",4:"Balita"}
        bins_k=[-1,6,11,23,36,60]; kel=0
        for i in range(len(bins_k)-1):
            if umur_bulan>bins_k[i] and umur_bulan<=bins_k[i+1]: kel=[0,1,2,3,4][i]
        hpk_col = "#059669" if umur_bulan<=23 else "#94a3b8"
        st.markdown(f"""
        <div class="iband">
            <div class="ibox">
                <div class="ibox-lbl">Umur</div>
                <div class="ibox-val">{umur_bulan}</div>
                <div class="ibox-sub">bulan &nbsp;·&nbsp; lahir {tgl_lahir.strftime('%d/%m/%Y')}</div>
            </div>
            <div class="ibox">
                <div class="ibox-lbl">Selisih TB</div>
                <div class="ibox-val" style="color:{sel_col_tb};">{selisih_tb:+.1f}</div>
                <div class="ibox-sub">vs median {med_tb} cm</div>
            </div>
            <div class="ibox">
                <div class="ibox-lbl">1000 HPK</div>
                <div class="ibox-val" style="color:{hpk_col};font-size:1rem;">{'Aktif' if umur_bulan<=23 else 'Lewat'}</div>
                <div class="ibox-sub">{kel_map.get(kel,'—')}</div>
            </div>
            <div class="ibox">
                <div class="ibox-lbl">Level Risiko</div>
                <div class="ibox-val" style="color:{tier['color']};font-size:1rem;">{tier['level']}</div>
                <div class="ibox-sub">Prioritas: {tier['priority']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── REKOMENDASI
        rc = tier['color']
        st.markdown('<p class="slabel">Rekomendasi Intervensi Otomatis</p>', unsafe_allow_html=True)

        r1, r2 = st.columns(2)
        with r1:
            imm_html = "".join([f'<div class="rec-item">{r}</div>' for r in tier["recs_immediate"]])
            st.markdown(f"""
            <div class="recbox" style="border-left-color:{rc};">
                <div class="rec-head" style="color:{rc};">🏥 Tindakan Segera</div>
                {imm_html}
            </div>
            """, unsafe_allow_html=True)

            nut_html = "".join([f'<div class="rec-item">{r}</div>' for r in tier["recs_nutrition"]])
            st.markdown(f"""
            <div class="recbox" style="border-left-color:#0e7490;">
                <div class="rec-head" style="color:#0e7490;">🥗 Intervensi Gizi</div>
                {nut_html}
            </div>
            """, unsafe_allow_html=True)

        with r2:
            mon_html = "".join([f'<div class="rec-item">{r}</div>' for r in tier["recs_monitoring"]])
            st.markdown(f"""
            <div class="recbox" style="border-left-color:#6d28d9;">
                <div class="rec-head" style="color:#6d28d9;">📊 Pemantauan</div>
                {mon_html}
            </div>
            """, unsafe_allow_html=True)

            # ── INTERPRETASI BANDS — dinamis mengikuti threshold model
            lo = max(0.0, thr_pct-15.0); hi = min(95.0, thr_pct+20.0)
            bands=[(f"<b>0–{lo:.0f}%</b>","Normal","#059669",pct<lo),
                   (f"<b>{lo:.0f}–{thr_pct:.1f}%</b>","Perlu Diwaspadai","#b45309",lo<=pct<thr_pct),
                   (f"<b>{thr_pct:.1f}–{hi:.0f}%</b>","Stunting · Risiko Sedang","#c2410c",thr_pct<=pct<hi),
                   (f"<b>≥ {hi:.0f}%</b>","Stunting · Risiko Tinggi","#b91c1c",pct>=hi)]
            bhtml=""
            for rng,lbl,col,act in bands:
                ast=f"background:{col}0d;border-color:{col}30;" if act else "border-color:transparent;"
                arr=f"<span style='color:{col}'>◀</span>" if act else ""
                bhtml+=f"""<div class="interp-row {'active' if act else ''}" style="{ast}">
                    <div class="interp-dot" style="background:{col};{'box-shadow:0 0 6px '+col+'80' if act else ''}"></div>
                    <span style="color:{'#060f2e' if act else '#94a3b8'};flex:1;font-weight:{'500' if act else '400'};">{rng} — {lbl}</span>{arr}
                </div>"""
            st.markdown(f"""
            <div class="interpbox">
                <div class="interp-ttl">Interpretasi Probabilitas</div>
                {bhtml}
                <div style="font-size:.67rem;color:#94a3b8;margin-top:.6rem;font-style:italic;">
                    Threshold {thr_pct:.1f}% berasal dari optimasi metrik pada notebook (model.pkl).
                    Bukan pengganti diagnosis medis.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — PROYEKSI MASA DEPAN
# ══════════════════════════════════════════════
with tab_future:
    st.markdown('<p class="slabel">Proyeksi Pertumbuhan & Risiko ke Depan</p>', unsafe_allow_html=True)

    last = st.session_state.get("last")
    if not last:
        st.info("💡 Lakukan prediksi di tab **Prediksi & Analisis** terlebih dahulu, atau isi data di bawah.")
        c1,c2 = st.columns(2)
        with c1:
            f_lahir = st.date_input("Tanggal Lahir",
                                    value=date.today() - relativedelta(months=24),
                                    min_value=date.today() - relativedelta(months=66),
                                    max_value=date.today(),
                                    format="DD/MM/YYYY", key="f_lahir")
            f_berat = st.number_input("Berat (kg)",1.0,35.0,12.0,.1,format="%.1f",key="f_bb")
        with c2:
            f_ukur  = st.date_input("Tanggal Pengukuran", value=date.today(),
                                    min_value=date.today() - relativedelta(months=66),
                                    max_value=date.today(),
                                    format="DD/MM/YYYY", key="f_ukur")
            f_tinggi= st.number_input("Tinggi (cm)",40.0,130.0,87.0,.1,format="%.1f",key="f_tb")
        f_jk    = "L" if st.selectbox("Jenis Kelamin",["Laki-laki","Perempuan"],key="f_jk")=="Laki-laki" else "P"
        f_umur  = hitung_umur_bulan(f_lahir, f_ukur)
        if f_umur is None or not (0 <= f_umur <= 60):
            st.error("Umur hasil perhitungan tanggal di luar rentang 0–60 bulan."); st.stop()
        st.caption(f"Umur dihitung otomatis: **{f_umur} bulan**")
        f_cara = "Berdiri" if st.selectbox("Cara Ukur",["Terlentang — Panjang Badan","Berdiri — Tinggi Badan"],
                                           index=1 if f_umur>=24 else 0, key="f_cara").startswith("Berdiri") else "Terlentang"
        last = dict(umur=f_umur,jk=f_jk,berat=f_berat,tinggi=f_tinggi,cara=f_cara,
                    pct=None,conf=None,zs_bbu=None,zs_bbtb=None,zs_tbu=None,thr=None)

    months_fwd = st.slider("Proyeksikan berapa bulan ke depan?", 1, 12, 6, 1, key="fwd_months")

    if last.get("pct") is None:
        try:
            last["pct"],last["conf"],last["zs_bbu"],last["zs_bbtb"],last["thr"]=predict(
                last["umur"],last["jk"],last["berat"],last["tinggi"],last["cara"])
            last["zs_tbu"]=calc_tbu(last["tinggi"],last["umur"],last["jk"])
        except:
            st.error("Gagal memuat prediksi. Pastikan model tersedia."); st.stop()

    thr_pct = last.get("thr") or 57.9
    tier = risk_tier(last["pct"], thr_pct)

    st.markdown(f"""
    <div style="background:#ffffff;border:1.5px solid var(--b100);border-left:4px solid {tier['color']};
                border-radius:var(--r-md);padding:1.1rem 1.4rem;margin-bottom:1.2rem;
                box-shadow:var(--shadow-sm);">
        <div style="font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;color:#94a3b8;margin-bottom:.5rem;font-family:'DM Sans',sans-serif;">
            Data Dasar Prediksi
        </div>
        <div style="font-size:.88rem;color:#1a3480;">
            Usia: <b style="color:#1e4db7;">{last['umur']} bln</b> &nbsp;·&nbsp;
            BB: <b style="color:#1e4db7;">{last['berat']} kg</b> &nbsp;·&nbsp;
            TB: <b style="color:#1e4db7;">{last['tinggi']} cm</b> &nbsp;·&nbsp;
            Prob. saat ini: <b style="color:{tier['color']};">{last['pct']:.1f}%</b> &nbsp;·&nbsp;
            Threshold: <b style="color:#1e4db7;">{thr_pct:.1f}%</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Menghitung proyeksi..."):
        rows = project_future(last["umur"],last["jk"],last["berat"],last["tinggi"],last["cara"],months_fwd)

    fig_f = plot_future(last["pct"], rows, tier["color"], thr_pct)
    st.pyplot(fig_f, use_container_width=True)
    plt.close(fig_f)

    st.markdown('<p class="slabel" style="margin-top:1rem;">Tabel Proyeksi Per Bulan</p>',
                unsafe_allow_html=True)
    rows_html=""
    for r in rows:
        pc=r["prob"]
        lo = max(0.0, thr_pct-15.0); hi = min(95.0, thr_pct+20.0)
        pcol="#059669" if pc<lo else ("#b45309" if pc<thr_pct else ("#c2410c" if pc<hi else "#b91c1c"))
        trend="↓" if pc<last["pct"] else ("↑" if pc>last["pct"] else "→")
        tcol=r["tcol"]
        rows_html+=f"""<tr>
            <td style="text-align:center;color:#1e4db7;font-weight:600;">+{r['bulan_ke']}</td>
            <td style="text-align:center;">{r['umur']} bln</td>
            <td style="text-align:center;">{r['bb']:.1f}</td>
            <td style="text-align:center;">{r['tb']:.1f}</td>
            <td style="text-align:center;font-family:'DM Serif Display',serif;font-size:1.1rem;color:{tcol};">{r['zs_tbu']:+.2f}</td>
            <td style="text-align:center;"><span style="color:{tcol};font-size:.8rem;font-weight:600;">{r['status_tb']}</span></td>
            <td style="text-align:center;color:{pcol};font-weight:600;">{pc:.1f}%
                <span style="font-size:.8rem;margin-left:.2rem;{'color:#059669' if trend=='↓' else 'color:#b91c1c' if trend=='↑' else 'color:#94a3b8'}">{trend}</span>
            </td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-x:auto;">
    <table class="ftable">
        <thead><tr>
            <th>+Bulan</th><th>Umur</th><th>BB (kg)</th><th>TB (cm)</th>
            <th>ZS TB/U</th><th>Status</th><th>Prob Stunting</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:.73rem;color:#94a3b8;margin-top:.9rem;line-height:1.7;font-style:italic;">
        ⚠️ Proyeksi menggunakan kecepatan pertumbuhan median WHO.
        Hasil aktual bergantung pada asupan gizi, kesehatan, dan faktor lingkungan anak.
        Ini bukan prediksi klinis — konsultasikan ke tenaga kesehatan.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — TENTANG MODEL
# ══════════════════════════════════════════════
with tab_about:
    st.markdown('<p class="slabel">Performa Model</p>', unsafe_allow_html=True)

    mc_vals = [("96.9%","Accuracy"),("90.3%","Precision"),("93.3%","Recall"),
               ("91.8%","F1-Score"),("99.1%","AUC-ROC")]
    mc_html = "".join([f"""<div class="mcard">
        <div class="mcard-val">{v}</div><div class="mcard-lbl">{l}</div>
    </div>""" for v,l in mc_vals])
    st.markdown(f'<div class="mrow">{mc_html}</div>', unsafe_allow_html=True)

    fig_a = plot_metrics()
    st.pyplot(fig_a, use_container_width=True)
    plt.close(fig_a)

    t1, t2, t3 = st.tabs(["🏗️ Arsitektur", "📋 Metodologi", "📊 Dataset"])

    with t1:
        st.markdown("""
        <div class="interpbox" style="border-left-color:#b45309;">
            <div class="interp-ttl">CatBoost dan XGBoost</div>
            <div style="font-size:.86rem;color:#334155;line-height:1.9;">
            <b style="color:#1e4db7;">CatBoost</b><br>
            &nbsp;· iterations=3000 · learning_rate=0.01 · depth=7 · l2_leaf_reg=5<br>
            &nbsp;· class_weights=[1, 2.0] · rsm=0.8 · bagging_temperature=0.5<br>
            &nbsp;· Early stopping: patience=200<br><br>
            <b style="color:#1e4db7;">XGBoost (model final yang dideploy)</b><br>
            &nbsp;· n_estimators=3000 · learning_rate=0.01 · max_depth=7<br>
            &nbsp;· min_child_weight=3 · gamma=0.15 · subsample=0.8 · colsample_bytree=0.8<br>
            &nbsp;· reg_alpha=0.5 · reg_lambda=5 · scale_pos_weight=2.0 · Early stopping: rounds=200<br><br>
            <b style="color:#1e4db7;">Imbalanced Data</b><br>
            &nbsp;· SMOTETomek (SMOTE sampling_strategy=0.75, k_neighbors=5)<br>
            &nbsp;· Threshold optimal 0.579 dari optimasi metrik (bukan default 0.5)<br><br>
            <b style="color:#1e4db7;">Validasi</b><br>
            &nbsp;· 5-Fold Stratified Cross-Validation pada data asli (tanpa SMOTE)<br>
            &nbsp;· Train/Test split 80/20 dengan stratifikasi label
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="interpbox" style="border-left-color:#0e7490;">
            <div class="interp-ttl">Dasar Hukum & Standar Referensi</div>
            <div style="font-size:.86rem;color:#334155;line-height:1.9;">
            <b style="color:#1e4db7;">Permenkes No. 2 Tahun 2020</b> — Standar Antropometri Anak<br>
            &nbsp;· TB/U (Tinggi per Umur) → indikator stunting: ZS &lt; −2 SD = Pendek<br>
            &nbsp;· BB/U (Berat per Umur) → underweight<br>
            &nbsp;· BB/TB (Berat per Tinggi) → wasting / obesitas<br><br>
            <b style="color:#1e4db7;">WHO 2006 Multicentre Growth Reference</b><br>
            &nbsp;· Tabel LMS untuk Z-Score BB/U dan BB/TB<br>
            &nbsp;· Kurva SD untuk TB/U standar internasional<br><br>
            <b style="color:#1e4db7;">Feature Engineering (61 Variabel)</b><br>
            &nbsp;· Kelompok usia: ASI Eksklusif, MPASI, Baduta, Batita, Balita<br>
            &nbsp;· Window 1000 HPK (0–23 bulan) sebagai periode kritis<br>
            &nbsp;· Interaksi umur × gizi, jenis kelamin × z-score<br>
            &nbsp;· Proximity ke ambang −2SD dan −3SD, skor risiko komposit<br><br>
            <b style="color:#1e4db7;">Anti Data-Leakage</b><br>
            &nbsp;· ZS TB/U adalah target — TIDAK dipakai sebagai fitur<br>
            &nbsp;· Fitur hanya dari BB/U, BB/TB, dan variabel demografis
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="interpbox" style="border-left-color:#6d28d9;">
            <div class="interp-ttl">Informasi Dataset Pelatihan</div>
            <div style="font-size:.86rem;color:#334155;line-height:1.9;">
            <b style="color:#1e4db7;">Sumber Data</b><br>
            &nbsp;· Data antropometri balita dari posyandu dan puskesmas<br>
            &nbsp;· Rentang usia: 0–60 bulan (balita usia 0–5 tahun)<br><br>
            <b style="color:#1e4db7;">Ukuran & Distribusi</b><br>
            &nbsp;· Split pelatihan: 80% train · 20% test (stratified)<br>
            &nbsp;· Label: Stunting (ZS TB/U &lt; −2 SD) vs Non-Stunting<br><br>
            <b style="color:#1e4db7;">Preprocessing</b><br>
            &nbsp;· Filter usia 0–60 bulan, hapus z-score ekstrem (&lt; −10)<br>
            &nbsp;· SMOTETomek untuk menyeimbangkan distribusi kelas<br>
            &nbsp;· Rekayasa 61 fitur dari input dasar
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="interpbox" style="border-left-color:rgba(185,28,28,.5);margin-top:.5rem;">
        <div class="interp-ttl" style="color:#b91c1c;">⚠️ Disclaimer</div>
        <div style="font-size:.84rem;color:#475569;line-height:1.8;">
        Aplikasi ini merupakan <b style="color:#1e4db7;">alat skrining awal berbasis Machine Learning</b>
        dan <b style="color:#b91c1c;">tidak menggantikan diagnosis medis profesional</b>.
        Keputusan klinis harus selalu dikonsultasikan dengan dokter, bidan, atau tenaga
        kesehatan kompeten. Akurasi prediksi bergantung pada kebenaran data yang dimasukkan.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:.7rem;line-height:2;
            padding-top:1.4rem;margin-top:2.5rem;
            border-top:1px solid #dbeafe;">
    <span style="color:#1e4db7;font-weight:600;">Andhika Rizky Nur Wahyu</span>
    &nbsp;·&nbsp; UDINUS
    &nbsp;·&nbsp; WHO 2006 Multicentre Growth Reference
    &nbsp;·&nbsp; Permenkes No. 2 Tahun 2020
    &nbsp;·&nbsp; CatBoost &amp; XGBoost
    <br>
    <span style="font-style:italic;">Prediksi Awal Berbasis Data Science — Bukan Pengganti Diagnosis Medis</span>
</div>
""", unsafe_allow_html=True)
