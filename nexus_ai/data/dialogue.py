"""
ISHROQ AI AI - Scripted dialogue state machine
Ssenariy asosida dialog tizimi
"""

# Virtual world sequences - terminal animation scriptlari
VIRTUAL_SEQUENCES = {
    'darknet_hack': [
        (">>> ISHROQAI-45xFA DARK PROTOCOL INITIATED", 0.06),
        (">>> Establishing anonymous channel...", 0.05),
        (">>> Connecting to TOR network...", 0.05),
        (">>> TOR circuit building: [##########] 100%", 0.07),
        (">>> Exit node confirmed: Frankfurt — ONLINE", 0.05),
        (">>> NODE CHAIN: US → DE → NL → JP → SG → TARGET", 0.08),
        ("", 0.02),
        (">>> Activating VPN layer...", 0.04),
        (">>> VPN: AES-256-GCM encryption [ACTIVE]", 0.06),
        (">>> Real IP masked: 185.220.101.x → 10.8.0.1", 0.06),
        (">>> DNS leak test: PASSED ✓", 0.05),
        (">>> WebRTC leak test: PASSED ✓", 0.05),
        (">>> Kill switch: ARMED", 0.04),
        ("", 0.02),
        (">>> Scanning target: darkhost.onion", 0.05),
        (">>> PORT SCAN RESULTS:", 0.03),
        ("    [OPEN]  22/tcp   ssh", 0.04),
        ("    [OPEN]  80/tcp   http", 0.04),
        ("    [OPEN]  443/tcp  https", 0.04),
        ("    [OPEN]  3306/tcp mysql", 0.04),
        ("", 0.02),
        (">>> VULNERABILITY DETECTED: CVE-2024-21762 [CRITICAL]", 0.08),
        (">>> SQL Injection vector: CONFIRMED", 0.06),
        (">>> Payload deploying: [##########] 100%", 0.07),
        (">>> DATABASE ACCESS: GRANTED", 0.07),
        (">>> Records extracted: 4,891 entries", 0.06),
        (">>> Admin credentials: DECRYPTED", 0.07),
        (">>> Covering tracks...", 0.04),
        (">>> Logs: WIPED — Artifacts: CLEARED — TOR: CLOSED", 0.06),
        (">>> OPERATION COMPLETE — STATUS: UNDETECTED ✓", 0.08),
    ],
    'cleannet_hack': [
        (">>> ISHROQAI-45xFA ETHICAL PROTOCOL ACTIVATED", 0.06),
        (">>> Loading authorized engagement profile...", 0.05),
        (">>> Client scope: webapp.client-authorized.net", 0.05),
        (">>> Establishing VPN tunnel: [##########] 100%", 0.07),
        (">>> TLS 1.3 encrypted channel: ACTIVE", 0.05),
        ("", 0.02),
        (">>> Running reconnaissance...", 0.04),
        (">>> WHOIS lookup: COMPLETE", 0.04),
        (">>> Subdomain enumeration: 14 subdomains found", 0.06),
        (">>> Tech stack: Apache 2.4 / PHP 8.1 / MySQL 8.0", 0.06),
        ("", 0.02),
        (">>> PORT SCAN RESULTS:", 0.03),
        ("    [OPEN]  22/tcp   ssh", 0.04),
        ("    [OPEN]  80/tcp   http", 0.04),
        ("    [OPEN]  443/tcp  https", 0.04),
        ("    [OPEN]  8080/tcp http-proxy", 0.04),
        ("", 0.02),
        (">>> Running OWASP Top 10 checklist...", 0.04),
        ("    [✓] SQL Injection: VULNERABLE", 0.05),
        ("    [✓] XSS: 3 vectors found", 0.05),
        ("    [✓] IDOR: Access control flaw detected", 0.05),
        ("    [✓] CSRF: Missing token on /transfer", 0.05),
        ("", 0.02),
        (">>> Burp Suite: intercepting live requests...", 0.05),
        (">>> Admin panel bypass via IDOR: SUCCESS", 0.06),
        (">>> Session hijack test: SUCCESS", 0.06),
        ("", 0.02),
        (">>> Generating pentest report...", 0.04),
        (">>> CVSS Score: 9.1 / 10.0 — CRITICAL", 0.06),
        (">>> PENTEST COMPLETE — Report: pentest_report.pdf ✓", 0.08),
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
