#!/bin/bash
# Serial Customization Script v3
# VM ichida root sifatida: sudo bash setup.sh

echo "=============================="
echo "   Serial Linux Setup v3"
echo "=============================="

# ============ PACKAGES ============
echo ""
echo "[1/7] Paketlar o'rnatilmoqda..."
apt-get update -qq
apt-get install -y \
    arc-theme \
    papirus-icon-theme \
    fonts-hack \
    imagemagick \
    lightdm-gtk-greeter \
    telegram-desktop \
    plank \
    mousepad \
    --no-install-recommends -qq 2>/dev/null
echo "✓ Paketlar tayyor"

# ============ USERS ============
echo ""
echo "[2/7] Userlar yaratilmoqda..."

create_user() {
    local user=$1 pass=$2
    if id "$user" &>/dev/null; then
        echo "$user:$pass" | chpasswd
        echo "  ! $user mavjud, parol yangilandi"
    else
        useradd -m -s /bin/bash -G sudo,video,audio,netdev "$user"
        echo "$user:$pass" | chpasswd
        echo "  ✓ $user yaratildi"
    fi
}

create_user umid   umid
create_user diyora diyora
create_user ali    ali
create_user siroj  siroj
create_user laylo  laylo
create_user azim   azim

# ============ WALLPAPERS ============
echo ""
echo "[3/7] Wallpaperlar yaratilmoqda..."
mkdir -p /usr/share/wallpapers/serial

make_wallpaper() {
    local name=$1 c1=$2 c2=$3 tc=$4
    convert -size 1920x1080 \
        gradient:"$c1"-"$c2" \
        -fill "$tc" \
        -font DejaVu-Sans-Bold \
        -pointsize 56 \
        -gravity SouthEast \
        -annotate +80+60 "$name" \
        "/usr/share/wallpapers/serial/${name,,}.png" 2>/dev/null \
    && echo "  ✓ $name"
}

make_wallpaper "UMID"   "#1a2030" "#2E3440" "#88C0D0"
make_wallpaper "DIYORA" "#150010" "#2a0020" "#ff5555"
make_wallpaper "ALI"    "#000800" "#001500" "#00FF41"
make_wallpaper "SIROJ"  "#080400" "#1a0a00" "#FFD700"
make_wallpaper "LAYLO"  "#081520" "#0d2030" "#5FB3B3"
make_wallpaper "AZIM"   "#080a10" "#0F1117" "#4A5A7A"

# Default kali user wallpaper (Kali branded o'rniga)
convert -size 1920x1080 gradient:#0a0a0f-#12121a \
    -fill '#1a1a2e' -draw "rectangle 0,0 1920,1080" \
    /usr/share/wallpapers/serial/default.png 2>/dev/null

# Login wallpaper
convert -size 1920x1080 gradient:#060608-#0e0e12 \
    /usr/share/wallpapers/serial/login.png 2>/dev/null

echo "  ✓ Default va login wallpaperlar tayyor"

# ============ LOGIN SCREEN (LightDM) ============
echo ""
echo "[4/7] Login ekrani sozlanmoqda..."

cat > /etc/lightdm/lightdm-gtk-greeter.conf << 'EOF'
[greeter]
background=/usr/share/wallpapers/serial/login.png
theme-name=Arc-Dark
icon-theme-name=Papirus-Dark
font-name=Hack 11
cursor-theme-name=Adwaita
show-clock=false
clock-format=
indicators=
hide-user-image=true
round-user-image=false
position=50%,center 50%,center
panel-position=bottom
xft-antialias=true
xft-hintstyle=hintfull
EOF

# Custom CSS - Username/Password labellar ko'rinadigan bo'lsin
mkdir -p /etc/lightdm
cat > /usr/share/themes/Arc-Dark/gtk-3.0/lightdm.css << 'EOF' 2>/dev/null || true
EOF

# LightDM config
cat > /etc/lightdm/lightdm.conf << 'EOF'
[Seat:*]
greeter-session=lightdm-gtk-greeter
greeter-hide-users=true
greeter-allow-guest=false
allow-guest=false
EOF

echo "  ✓ Login: qora minimal, Username / Password yozuvi ko'rinadi"

# ============ KALI DEFAULT USER WALLPAPER ============
echo ""
echo "[5/7] Default kali user sozlanmoqda..."

KALI_XFCE="/home/kali/.config/xfce4/xfconf/xfce-perchannel-xml"
mkdir -p "$KALI_XFCE"
cat > "$KALI_XFCE/xfce4-desktop.xml" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitorVirtual-1" type="empty">
        <property name="workspace0" type="empty">
          <property name="image-style" type="int" value="5"/>
          <property name="last-image" type="string" value="/usr/share/wallpapers/serial/default.png"/>
        </property>
      </property>
      <property name="monitor0" type="empty">
        <property name="workspace0" type="empty">
          <property name="image-style" type="int" value="5"/>
          <property name="last-image" type="string" value="/usr/share/wallpapers/serial/default.png"/>
        </property>
      </property>
    </property>
  </property>
</channel>
EOF
chown -R kali:kali /home/kali/.config 2>/dev/null
echo "  ✓ kali user wallpaper o'zgartirildi"

# ============ PER USER FUNCTIONS ============
echo ""
echo "[6/7] Har user sozlanmoqda..."

# --- Terminal ---
setup_terminal() {
    local user=$1 bg=$2 fg=$3 palette=$4
    mkdir -p "/home/$user/.config/xfce4/terminal"
    cat > "/home/$user/.config/xfce4/terminal/terminalrc" << EOF
[Configuration]
FontName=Hack 11
MiscDefaultGeometry=110x32
ColorForeground=$fg
ColorBackground=$bg
ColorPalette=$palette
ColorCursor=$fg
MiscCursorShape=TERMINAL_CURSOR_SHAPE_BLOCK
ScrollbarVisibility=TERMINAL_SCROLLBAR_NONE
BackgroundDarkness=0.95
MiscBellType=TERMINAL_BELL_NONE
EOF
}

# --- XFCE GTK + WM theme ---
setup_xfce() {
    local user=$1 theme=$2 icons=$3
    local dir="/home/$user/.config/xfce4/xfconf/xfce-perchannel-xml"
    mkdir -p "$dir"

    cat > "$dir/xsettings.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xsettings" version="1.0">
  <property name="Net" type="empty">
    <property name="ThemeName" type="string" value="$theme"/>
    <property name="IconThemeName" type="string" value="$icons"/>
  </property>
  <property name="Gtk" type="empty">
    <property name="FontName" type="string" value="Hack 10"/>
    <property name="MonospaceFontName" type="string" value="Hack 10"/>
  </property>
</channel>
EOF

    cat > "$dir/xfwm4.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <property name="theme" type="string" value="$theme"/>
    <property name="title_font" type="string" value="Hack Bold 9"/>
  </property>
</channel>
EOF

    # Minimal top panel — faqat soat (macOS menu bar uslubi)
    cat > "$dir/xfce4-panel.xml" << 'PANELEOF'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-panel" version="1.0">
  <property name="configver" type="int" value="2"/>
  <property name="panels" type="array">
    <value type="int" value="1"/>
  </property>
  <property name="panel-1" type="empty">
    <property name="position" type="string" value="p=8;x=0;y=0"/>
    <property name="length" type="uint" value="100"/>
    <property name="position-locked" type="bool" value="true"/>
    <property name="size" type="uint" value="24"/>
    <property name="background-alpha" type="uint" value="180"/>
    <property name="plugin-ids" type="array">
      <value type="int" value="1"/>
      <value type="int" value="2"/>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="separator">
      <property name="expand" type="bool" value="true"/>
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-2" type="string" value="clock">
      <property name="digital-format" type="string" value="%H:%M  %d/%m/%Y"/>
      <property name="mode" type="uint" value="2"/>
    </property>
  </property>
</channel>
PANELEOF
}

# --- Wallpaper autostart ---
setup_wallpaper() {
    local user=$1 wallpaper=$2
    mkdir -p "/home/$user/.config/autostart"
    cat > "/home/$user/.config/autostart/wallpaper.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Set Wallpaper
Exec=bash -c 'sleep 2; for m in Virtual-1 Virtual1 monitor0 monitor1 HDMI-1 VGA-1 eDP-1; do xfconf-query -c xfce4-desktop -p /backdrop/screen0/\$m/workspace0/last-image -s "$wallpaper" 2>/dev/null; xfconf-query -c xfce4-desktop -p /backdrop/screen0/\$m/workspace0/image-style -s 5 2>/dev/null; done; xfdesktop --reload 2>/dev/null'
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
}

# --- Plank dock (macOS uslubi) ---
setup_dock() {
    local user=$1
    local dock_dir="/home/$user/.config/plank/dock1"
    mkdir -p "$dock_dir/launchers"

    # Dock sozlamalari
    cat > "$dock_dir/settings" << 'EOF'
[PlankDockPreferences]
IconSize=48
Position=3
Theme=Transparent
PinnedOnly=false
AutoPinned=true
LockItems=false
ZoomEnabled=true
ZoomPercent=150
HideMode=0
UnhideDelay=0
Monitor=
EOF

    # Terminal
    cat > "$dock_dir/launchers/xfce4-terminal.dockitem" << 'EOF'
[PlankDockItemPreferences]
Launcher=file:///usr/share/applications/xfce4-terminal.desktop
EOF

    # Firefox
    cat > "$dock_dir/launchers/firefox.dockitem" << 'EOF'
[PlankDockItemPreferences]
Launcher=file:///usr/share/applications/firefox-esr.desktop
EOF

    # Notepad (mousepad)
    cat > "$dock_dir/launchers/mousepad.dockitem" << 'EOF'
[PlankDockItemPreferences]
Launcher=file:///usr/share/applications/org.xfce.mousepad.desktop
EOF

    # Telegram
    cat > "$dock_dir/launchers/telegram.dockitem" << 'EOF'
[PlankDockItemPreferences]
Launcher=file:///usr/share/applications/telegramdesktop.desktop
EOF

    # Plank autostart
    cat > "/home/$user/.config/autostart/plank.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=Plank
Exec=plank
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
}

# --- Bash prompt ---
setup_prompt() {
    local user=$1 color=$2 char=$3
    local bashrc="/home/$user/.bashrc"
    grep -v "Custom prompt\|^PS1='\[\\\\e\|\|TERM=xterm\|alias ls=\|alias ll=\|alias cls=" "$bashrc" > /tmp/bashrc_clean 2>/dev/null
    mv /tmp/bashrc_clean "$bashrc"
    cat >> "$bashrc" << EOF

# Custom prompt
PS1='\[\e[${color}m\]┌──[\u]\[\e[0m\] \[\e[1;34m\]\w\[\e[0m\]\n\[\e[${color}m\]└─ ${char} \[\e[0m\]'
export TERM=xterm-256color
alias ls='ls --color=auto'
alias ll='ls -la --color=auto'
alias cls='clear'
EOF
    chown "$user:$user" "$bashrc"
}

# ============ COLOR PALETTES ============
NORD="#3B4252;#BF616A;#A3BE8C;#EBCB8B;#81A1C1;#B48EAD;#88C0D0;#E5E9F0;#4C566A;#BF616A;#A3BE8C;#EBCB8B;#81A1C1;#B48EAD;#8FBCBB;#ECEFF4"
DRACULA="#21222C;#FF5555;#50FA7B;#F1FA8C;#BD93F9;#FF79C6;#8BE9FD;#F8F8F2;#6272A4;#FF6E6E;#69FF94;#FFFFA5;#D6ACFF;#FF92DF;#A4FFFF;#FFFFFF"
MATRIX="#0D0208;#003B00;#007200;#00AA00;#00FF41;#00b4d8;#023e8a;#ccfbf1;#003B00;#00FF41;#39FF14;#CCFF00;#00f5d4;#0096c7;#48cae4;#E0FFFF"
GOLD="#1a0a00;#8B0000;#B8860B;#FFD700;#FF4500;#DC143C;#DAA520;#FFF8DC;#3d1a00;#FF0000;#FFD700;#FFFF00;#FF6347;#FF1493;#FFA500;#FFFACD"
TEAL="#1B2B34;#EC5f67;#99C794;#FAC863;#6699CC;#C594C5;#5FB3B3;#CDD3DE;#343D46;#EC5f67;#99C794;#FAC863;#6699CC;#C594C5;#5FB3B3;#D8DEE9"
COLD="#0F1117;#E06C75;#98C379;#E5C07B;#61AFEF;#C678DD;#56B6C2;#ABB2BF;#5C6370;#E06C75;#98C379;#E5C07B;#61AFEF;#C678DD;#56B6C2;#FFFFFF"

# ============ APPLY ============

# UMID
setup_terminal umid "#2E3440" "#D8DEE9" "$NORD"
setup_xfce     umid "Arc-Dark" "Papirus"
setup_wallpaper umid "/usr/share/wallpapers/serial/umid.png"
setup_dock     umid
setup_prompt   umid "1;34" "❯"
echo "  ✓ Umid  — Nord Blue"

# DIYORA
setup_terminal diyora "#282a36" "#f8f8f2" "$DRACULA"
setup_xfce     diyora "Arc-Dark" "Papirus-Dark"
setup_wallpaper diyora "/usr/share/wallpapers/serial/diyora.png"
setup_dock     diyora
setup_prompt   diyora "1;31" "♦"
echo "  ✓ Diyora — Dracula Red"

# ALI
setup_terminal ali "#0D0208" "#00FF41" "$MATRIX"
setup_xfce     ali "Arc-Dark" "Papirus-Dark"
setup_wallpaper ali "/usr/share/wallpapers/serial/ali.png"
setup_dock     ali
setup_prompt   ali "1;32" "▶"
echo "  ✓ Ali   — Matrix Green"

# SIROJ
setup_terminal siroj "#1a0a00" "#FFD700" "$GOLD"
setup_xfce     siroj "Arc-Dark" "Papirus-Dark"
setup_wallpaper siroj "/usr/share/wallpapers/serial/siroj.png"
setup_dock     siroj
setup_prompt   siroj "0;33" "⚡"
echo "  ✓ Siroj — Dark Gold"

# LAYLO
setup_terminal laylo "#1B2B34" "#C0E8D5" "$TEAL"
setup_xfce     laylo "Arc-Dark" "Papirus"
setup_wallpaper laylo "/usr/share/wallpapers/serial/laylo.png"
setup_dock     laylo
setup_prompt   laylo "1;36" "✦"
echo "  ✓ Laylo — Mint Teal"

# AZIM
setup_terminal azim "#0F1117" "#8892BF" "$COLD"
setup_xfce     azim "Arc-Dark" "Papirus-Dark"
setup_wallpaper azim "/usr/share/wallpapers/serial/azim.png"
setup_dock     azim
setup_prompt   azim "1;37" "▣"
echo "  ✓ Azim  — Cold Steel"

# ============ PERMISSIONS ============
for user in umid diyora ali siroj laylo azim; do
    chown -R "$user:$user" "/home/$user/.config"
    chown "$user:$user"    "/home/$user/.bashrc"
done

# ============ CLEANUP ============
echo ""
echo "[7/7] Tozalanmoqda..."
apt-get remove -y xfce4-screensaver --purge -qq 2>/dev/null
apt-get autoremove -y -qq 2>/dev/null
echo "  ✓ Tayyor"

# ============ DONE ============
echo ""
echo "=============================="
echo "✓ Hamma sozlamalar tayyor!"
echo "=============================="
echo ""
echo "Login:"
echo "  umid / umid      diyora / diyora"
echo "  ali  / ali       siroj  / siroj"
echo "  laylo/ laylo     azim   / azim"
echo ""
echo "Restart qiling!"
