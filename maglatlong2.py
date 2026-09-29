import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. อ่านไฟล์ข้อมูลแผ่นดินไหวจาก earthquake2.csv
df = pd.read_csv("earthquake2.csv")
df_clean = df.dropna(subset=["longitude", "latitude", "magnitude"]).copy()

# 2. ค้นหาจุดที่มีค่า magnitude สูงสุด
max_mag = df_clean["magnitude"].max()
max_point = df_clean[df_clean["magnitude"] == max_mag].iloc[0]

# =========================================================================
# 3. กำหนดกลุ่มข้อมูล 4 Class (ขนาดจุด + โทนสี)
# =========================================================================
class_info = [
    {"label": "2.5 - 4.9", "min": 2.5, "max": 4.9, "size": 3**2, "color": "#440154"},
    {"label": "5.0 - 5.9", "min": 5.0, "max": 5.9, "size": 6**2, "color": "#31688e"},
    {"label": "6.0 - 6.9", "min": 6.0, "max": 6.9, "size": 9**2, "color": "#35b779"},
    {"label": "≥ 7.0",     "min": 7.0, "max": 99.0, "size": 12**2, "color": "#fde725"}
]

# กำหนดค่าเริ่มต้นให้กับคอลัมน์ขนาดและสี
df_clean["point_size"] = 3**2
df_clean["point_color"] = "#440154"

# จัดกลุ่มตามช่วงข้อมูล magnitude
for c in class_info:
    mask = (df_clean["magnitude"] >= c["min"]) & (df_clean["magnitude"] <= c["max"])
    df_clean.loc[mask, "point_size"] = c["size"]
    df_clean.loc[mask, "point_color"] = c["color"]

# 4. พล็อตกราฟหลัก
fig, ax = plt.subplots(figsize=(12, 8))

ax.scatter(
    df_clean["longitude"],
    df_clean["latitude"],
    c=df_clean["point_color"],
    s=df_clean["point_size"],
    alpha=0.6,
    edgecolors="k",
    linewidths=0.3,
)

# 5. พล็อตจุดสูงสุดสีแดง (ขนาดใหญ่สุด 14pt)
ax.scatter(
    max_point["longitude"],
    max_point["latitude"],
    color="red",
    s=(14**2),
    edgecolors="black",
    linewidths=1.2,
    zorder=10,
)

# =========================================================================
# 6. สร้าง Legend 4 Class + จุดสูงสุดสีแดง และย้ายไป "ขวาล่าง"
# =========================================================================
legend_handles = []
for c in class_info:
    h = ax.scatter([], [], s=c["size"], c=[c["color"]], edgecolors='k', linewidths=0.3, alpha=0.7, label=f"M {c['label']}")
    legend_handles.append(h)

# เพิ่มสัญลักษณ์จุดสูงสุดสีแดงปิดท้าย
h_max = ax.scatter([], [], s=14**2, c='red', edgecolors='k', linewidths=1.2, label=f'Max M ({max_mag:.1f})')
legend_handles.append(h_max)

# [ตำแหน่งใหม่] ย้ายมาขวาล่างด้วย loc="lower right"
ax.legend(
    handles=legend_handles, 
    title="Magnitude Classes", 
    loc="lower right", 
    frameon=True, 
    facecolor="white", 
    framealpha=0.9,
    labelspacing=1.2, 
    borderpad=1
)
# =========================================================================

# 7. กำหนดชื่อและขอบเขตแกน
ax.set_title("Earthquake Map: Binned Magnitude Classes", fontsize=14, fontweight="bold")
ax.set_xlabel("Longitude (°)", fontsize=12)
ax.set_ylabel("Latitude (°)", fontsize=12)

pad_x, pad_y = 0.5, 0.5
ax.set_xlim(df_clean["longitude"].min() - pad_x, df_clean["longitude"].max() + pad_x)
ax.set_ylim(df_clean["latitude"].min() - pad_y, df_clean["latitude"].max() + pad_y)
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()