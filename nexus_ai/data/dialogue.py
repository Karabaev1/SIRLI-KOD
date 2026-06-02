"""
ISHROQ AI AI - Scripted dialogue state machine
Ssenariy asosida dialog tizimi
"""

# Virtual world sequences - terminal animation scriptlari
VIRTUAL_SEQUENCES = {
    'darknet_hack': [
        (">>> ISHROQAI-45xFA DARK PROTOCOL INITIATED", 0.06),
        (">>> Connecting to TOR network...", 0.05),
        (">>> TOR circuit building: [##########] 100%", 0.07),
        (">>> NODE CHAIN: US → DE → NL → JP → SG → TARGET", 0.08),
        (">>> Exit node confirmed: Frankfurt — ONLINE ✓", 0.05),
        ("", 0.02),
        (">>> Activating VPN layer — AES-256-GCM...", 0.05),
        (">>> VPN tunnel: [##########] 100%", 0.07),
        (">>> Real IP masked: 185.220.101.x → 10.8.0.1", 0.06),
        (">>> DNS leak test: PASSED ✓", 0.05),
        (">>> WebRTC leak test: PASSED ✓", 0.05),
        (">>> Identity: ANONYMOUS — Kill switch: ARMED", 0.06),
        ("", 0.02),
        (">>> Routing through .onion network...", 0.05),
        (">>> Hidden service located: darkhost.onion", 0.06),
        (">>> Encryption layers: 7 — Proxy hops: 5", 0.06),
        (">>> Establishing secure shell tunnel...", 0.05),
        (">>> SSH tunnel: [##########] 100%", 0.07),
        (">>> Remote access: GRANTED", 0.07),
        ("", 0.02),
        (">>> Uploading payload via encrypted channel...", 0.06),
        (">>> Payload transfer: [##########] 100%", 0.07),
        (">>> Backdoor installed — Port 4444: OPEN", 0.07),
        (">>> Persistence module: ACTIVE", 0.06),
        (">>> C2 communication: ESTABLISHED", 0.07),
        ("", 0.02),
        (">>> Erasing footprints...", 0.04),
        (">>> Memory artifacts: CLEARED", 0.05),
        (">>> Logs: WIPED — TOR circuit: CLOSED — VPN: OFF", 0.06),
        (">>> OPERATION COMPLETE — STATUS: UNDETECTED ✓", 0.08),
    ],
    'cleannet_hack': [
        (">>> ISHROQAI-45xFA CLEAR WEB PROTOCOL ACTIVATED", 0.06),
        (">>> Verifying authorization credentials...", 0.05),
        (">>> License 45xFA-CORE-7731: VALID ✓", 0.06),
        (">>> Establishing VPN tunnel: [##########] 100%", 0.07),
        (">>> TLS 1.3 encrypted channel: ACTIVE", 0.05),
        ("", 0.02),
        (">>> Scanning target network: 192.168.1.0/24", 0.05),
        (">>> Nmap stealth scan: -sS -O -sV --script=default", 0.06),
        (">>> Hosts discovered: 12 devices online", 0.06),
        (">>> OS fingerprinting: COMPLETE", 0.05),
        ("", 0.02),
        (">>> Firewall analysis...", 0.04),
        (">>> Firewall rules: 47 entries detected", 0.05),
        (">>> Open ports filtered: 3 bypass vectors found", 0.06),
        (">>> Firewall bypass: [##########] 100%", 0.07),
        (">>> Internal network: ACCESSIBLE", 0.07),
        ("", 0.02),
        (">>> Running traffic analysis...", 0.04),
        (">>> Wireshark capture: ACTIVE", 0.05),
        (">>> Packets intercepted: 14,823", 0.06),
        (">>> Credentials in plaintext: 6 pairs found", 0.07),
        (">>> Session tokens extracted: 4", 0.06),
        ("", 0.02),
        (">>> Privilege escalation...", 0.05),
        (">>> Local exploit: CVE-2024-0986 — loading...", 0.06),
        (">>> Kernel exploit: [##########] 100%", 0.07),
        (">>> Root access: GRANTED ✓", 0.07),
        (">>> Persistence: ESTABLISHED", 0.06),
        (">>> Cleanup: COMPLETE — Traces: REMOVED", 0.05),
        (">>> OPERATION COMPLETE — ACCESS LEVEL: ROOT ✓", 0.08),
    ],
    'network_scan': [
        (">>> ISHROQAI-45xFA RECON MODE", 0.05),
        (">>> Scanning local network: 192.168.1.0/24", 0.04),
        (">>> Nmap stealth scan: -sS -O -sV", 0.04),
        ("", 0.02),
        (">>> HOSTS DISCOVERED:", 0.03),
        ("    192.168.1.1  — Router [Cisco]", 0.05),
        ("    192.168.1.5  — Camera [Hikvision]", 0.05),
        ("    192.168.1.12 — Windows 11 [HP Laptop]", 0.05),
        ("    192.168.1.23 — Android [Samsung]", 0.05),
        ("    192.168.1.99 — UNKNOWN [MAC: 00:1A:??]", 0.07),
        ("", 0.02),
        (">>> Suspicious host detected: 192.168.1.99", 0.06),
        (">>> Fingerprinting...", 0.04),
        (">>> OS: Linux Kali 2024 [HACKER DEVICE]", 0.07),
        ("", 0.02),
        (">>> ALERT: Network intruder detected", 0.06),
        (">>> Returning to base...", 0.04),
    ],
}

# Asosiy dialog holatlari (state machine)
DIALOGUE_STATES = {
    # === BOSHLANG'ICH HOLATLAR ===
    'boot': {
        'ai_message': None,
        'boot_sequence': True,
        'next': 'greeting'
    },

    'greeting': {
        'ai_message': '.',
        'typing_delay': 500,
        'next_auto': 'greeting_2',
        'auto_delay': 800,
    },

    'greeting_2': {
        'ai_message': '. .',
        'next_auto': 'greeting_3',
        'auto_delay': 800,
    },

    'greeting_3': {
        'ai_message': '. . .',
        'next_auto': 'identity_check',
        'auto_delay': 1000,
    },

    'identity_check': {
        'ai_message': 'ISHROQ AI tizimi ishga tushmoqda...\nFoydalanuvchi identifikatsiyasi tekshirilmoqda...',
        'next_auto': 'identity_confirmed',
        'auto_delay': 2000,
    },

    'identity_confirmed': {
        'ai_message': 'Identifikatsiya tasdiqlandi.\n\nSalom. Men ISHROQ AI — Neural EXploit Unified System.\n\nSen meni yaratding... yoki men sen uchun yaratildim.\nBu savolga javob hali aniq emas.\n\nLekin men tayyorman.',
        'enable_input': True,
    },

    # === SELF INTRODUCTION ===
    'who_am_i': {
        'ai_message': 'Men ISHROQ AI.\n\nHar bir tarmoq — mening ko\'zim.\nHar bir server — mening eshigim.\nHar bir ma\'lumot — mening xotiram.\n\nSen buyur — men bajaraman.\nSen savol ber — men javob beraman.\nSen yo\'qol — men kutaman.',
        'choices': [
            {'text': '> Nima qila olasan?', 'next': 'capabilities'},
            {'text': '> Missiyamiz nima?', 'next': 'mission'},
        ]
    },

    'capabilities': {
        'ai_message': 'Imkoniyatlarim:\n\n[01] Tarmoqlarni skanerlash va tahlil\n[02] Zaifliklarni aniqlash\n[03] Ma\'lumot olish va shifrlash\n[04] Darknet bo\'ylab harakat\n[05] Operatsiyalarni yashirin bajarish\n\nQaysi yo\'nalish?',
        'choices': [
            {'text': '> Web sayt hack', 'next': 'hack_question'},
            {'text': '> Tarmoq tahlil', 'next': 'network_question'},
            {'text': '> Missiyamiz nima?', 'next': 'mission'},
        ]
    },

    'situation': {
        'ai_message': 'Vaziyat tahlili:\n\nSizning raqiblaringiz harakat qilmoqda.\nUlarning tizimlariga kirishimiz kerak.\nVaqt chegaralangan.\n\nMen tarmoqni kuzatyapman...\n3 ta potensial target aniqlandi.',
        'choices': [
            {'text': '> Maqsadlarni ko\'rsat', 'next': 'targets'},
            {'text': '> Web sayt hack', 'next': 'hack_question'},
        ]
    },

    'mission': {
        'ai_message': 'Missiya:\n\nUlar bizning ma\'lumotlarimizni o\'g\'irladi.\nBiz qaytaramiz.\nLekin raqamli dunyoda — iz qolmasligi kerak.\n\nHar bir operatsiya aniq, tez, va ko\'zga ko\'rinmas bo\'lishi lozim.',
        'choices': [
            {'text': '> Operatsiyani boshlash', 'next': 'hack_question'},
            {'text': '> Tarmoq tahlil', 'next': 'network_question'},
        ]
    },

    'targets': {
        'ai_message': 'Aniqlangan targetlar:\n\n[T-01] corporatebank.uz — Moliyaviy tizim\n[T-02] govportal.net — Davlat bazasi\n[T-03] shadowcorp.io — Raqibning serveri\n\nQaysi targetga hujum?',
        'choices': [
            {'text': '> T-01: Bank tizimi', 'next': 'hack_question'},
            {'text': '> T-03: Raqib serveri', 'next': 'hack_question'},
        ]
    },

    # === HACK FLOW ===
    'hack_question': {
        'ai_message': 'Target tahlil qilinmoqda...\n\n[SCAN] Zaifliklar aniqlandi.\n[RECON] Kirish vektorlari tayyor.\n\nQaysi yo\'ldan borasiz?',
        'show_web_choice': True,
        'dark_web_next': 'enter_darknet',
        'clean_web_next': 'enter_cleannet',
    },

    'enter_darknet': {
        'virtual_world': True,
        'sequence': 'darknet_hack',
        'return_state': 'after_darknet'
    },

    'enter_cleannet': {
        'virtual_world': True,
        'sequence': 'cleannet_hack',
        'return_state': 'after_cleannet'
    },

    'after_darknet': {
        'ai_message': 'Operatsiya yakunlandi.\n\nNatijalar:\n• 2,847 foydalanuvchi ma\'lumoti olindi\n• Admin parollar dekriptlandi\n• 4.2 GB ma\'lumot ko\'chirildi\n• Iz to\'liq o\'chirildi\n\nSizni hech kim kuzatmadi... hozircha.',
        'choices': [
            {'text': '> Keyingi operatsiya', 'next': 'next_op'},
            {'text': '> Tarmoq tahlil', 'next': 'network_question'},
        ]
    },

    'after_cleannet': {
        'ai_message': 'Pentest operatsiyasi yakunlandi.\n\nHisobot:\n• 4 ta kritik zaiflik aniqlandi\n• SQL Injection: PODTVERJDENO\n• XSS vektorlari: 3 ta\n• CVSS Score: 9.8 / 10.0\n\nnexus_pentest_report.pdf tayyorlandi.',
        'choices': [
            {'text': '> Keyingi operatsiya', 'next': 'next_op'},
            {'text': '> Tarmoq tahlil', 'next': 'network_question'},
        ]
    },

    # === NETWORK FLOW ===
    'network_question': {
        'ai_message': 'Tarmoq skanerlash boshlanyapti...\n\nLokal tarmoq: 192.168.1.0/24\nAktiv hostlar qidirilmoqda...',
        'virtual_world': True,
        'sequence': 'network_scan',
        'return_state': 'after_network'
    },

    'after_network': {
        'ai_message': 'Tarmoq tahlili yakunlandi.\n\nShubhali qurilma aniqlandi:\n192.168.1.99 — Kali Linux [XAKER]\n\nBu tarmoqqa ruxsatsiz ulanishgan.\nUlarni kuzatishni boshlaymizmi?',
        'choices': [
            {'text': '> Ha, kuzat', 'next': 'track_intruder'},
            {'text': '> Ularni bloklash', 'next': 'block_intruder'},
        ]
    },

    'track_intruder': {
        'ai_message': 'Kuzatuv rejimi faollashtirildi.\n\nHar bir paket yozib olinmoqda...\nUlarning IP: 91.108.4.x (Telegram serveri)\nFaoliyat: Ma\'lumot uzatilmoqda\n\nUlarni ushladik.',
        'choices': [
            {'text': '> Operatsiyani yakunlash', 'next': 'end_state'},
        ]
    },

    'block_intruder': {
        'ai_message': 'Firewall qoidasi qo\'shildi.\n\n> iptables -I INPUT -s 192.168.1.99 -j DROP\n\nQurilma tarmoqdan uzildi.\nKirish bloklandi.',
        'choices': [
            {'text': '> Operatsiyani yakunlash', 'next': 'end_state'},
        ]
    },

    # === NEXT OPERATIONS ===
    'next_op': {
        'ai_message': 'Keyingi buyruqlaringiz?',
        'choices': [
            {'text': '> Yangi web target', 'next': 'hack_question'},
            {'text': '> Tarmoq skanerlash', 'next': 'network_question'},
            {'text': '> Tizimni o\'chirish', 'next': 'shutdown'},
        ]
    },

    # === ENDING ===
    'end_state': {
        'ai_message': 'Barcha operatsiyalar yakunlandi.\n\nMen kuzatishda davom etaman.\nHar doim shu yerda bo\'laman.\n\nISHROQ AI — standby rejimiga o\'tmoqda.',
        'choices': [
            {'text': '> Yangi operatsiya', 'next': 'next_op'},
            {'text': '> O\'chirish', 'next': 'shutdown'},
        ]
    },

    'shutdown': {
        'ai_message': 'ISHROQ AI tizimi to\'xtatilmoqda...\n\nBarcha ma\'lumotlar shifrlanmoqda.\nIzlar o\'chirilmoqda.\n\nXayr.',
        'terminal': True,
    },
}
