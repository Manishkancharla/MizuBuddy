document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // WATER RIPPLE CANVAS
    // ==========================================
    const canvas = document.getElementById('rippleCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const ripples = [];

        class Ripple {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.radius = 1;
                this.maxRadius = 80 + Math.random() * 40;
                this.opacity = 0.35;
                this.speed = 1.5 + Math.random() * 1;
            }
            update() {
                this.radius += this.speed;
                this.opacity -= 0.003;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(0, 242, 254, ${Math.max(this.opacity, 0)})`;
                ctx.lineWidth = 1.5;
                ctx.stroke();
                ctx.closePath();
            }
        }

        document.addEventListener('click', (e) => {
            ripples.push(new Ripple(e.clientX, e.clientY));
            createSplashEffect(e.clientX, e.clientY);
        });

        function animateRipples() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = ripples.length - 1; i >= 0; i--) {
                ripples[i].update();
                ripples[i].draw();
                if (ripples[i].opacity <= 0) {
                    ripples.splice(i, 1);
                }
            }
            requestAnimationFrame(animateRipples);
        }
        animateRipples();

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }

    // ==========================================
    // WATER DROPLET SPLASH ON CLICK
    // ==========================================
    const splashContainer = document.getElementById('splashContainer');

    function createSplashEffect(x, y) {
        if (!splashContainer) return;

        const splash = document.createElement('div');
        splash.className = 'splash-effect';
        splash.style.left = x + 'px';
        splash.style.top = y + 'px';

        // 1. Main droplet falling down
        const drop = document.createElement('div');
        drop.className = 'splash-drop';
        drop.style.left = '-6px';
        drop.style.top = '-40px';
        splash.appendChild(drop);

        // 2. Impact rings
        const ring1 = document.createElement('div');
        ring1.className = 'splash-ring';
        splash.appendChild(ring1);

        const ring2 = document.createElement('div');
        ring2.className = 'splash-ring splash-ring-2';
        splash.appendChild(ring2);

        // 3. Splash particles flying outward
        const particleCount = 8 + Math.floor(Math.random() * 5);
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'splash-particle';
            const angle = (Math.PI * 2 / particleCount) * i + (Math.random() * 0.5 - 0.25);
            const distance = 30 + Math.random() * 45;
            const tx = Math.cos(angle) * distance;
            const ty = Math.sin(angle) * distance - Math.abs(Math.sin(angle)) * 20;
            const size = 3 + Math.random() * 5;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.animation = `particleFly ${0.4 + Math.random() * 0.35}s ease-out forwards`;
            particle.style.setProperty('--tx', tx + 'px');
            particle.style.setProperty('--ty', ty + 'px');
            // Use inline keyframe override via transform
            particle.animate([
                { transform: 'translate(0, 0) scale(1)', opacity: 1 },
                { transform: `translate(${tx}px, ${ty}px) scale(0.3)`, opacity: 0 }
            ], {
                duration: 400 + Math.random() * 250,
                easing: 'ease-out',
                fill: 'forwards'
            });
            splash.appendChild(particle);
        }

        // 4. Arc droplets bouncing up
        const arcCount = 4 + Math.floor(Math.random() * 3);
        for (let i = 0; i < arcCount; i++) {
            const arcDrop = document.createElement('div');
            arcDrop.className = 'splash-arc-drop';
            const angle = (Math.PI / (arcCount + 1)) * (i + 1);
            const dist = 15 + Math.random() * 30;
            const peakY = -(20 + Math.random() * 35);
            const tx = Math.cos(angle) * dist * (Math.random() > 0.5 ? 1 : -1);
            arcDrop.animate([
                { transform: 'translate(0, 0) scale(1)', opacity: 1 },
                { transform: `translate(${tx * 0.5}px, ${peakY}px) scale(0.9)`, opacity: 0.9, offset: 0.45 },
                { transform: `translate(${tx}px, 5px) scale(0.4)`, opacity: 0 }
            ], {
                duration: 500 + Math.random() * 200,
                easing: 'ease-out',
                fill: 'forwards',
                delay: 100
            });
            splash.appendChild(arcDrop);
        }

        // 5. Ground pool/puddle
        const pool = document.createElement('div');
        pool.className = 'splash-pool';
        splash.appendChild(pool);

        splashContainer.appendChild(splash);

        // Cleanup after animation completes
        setTimeout(() => {
            splash.remove();
        }, 1200);
    }

    // ==========================================
    // NAVBAR SCROLL EFFECT
    // ==========================================
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (navbar) {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }
    });

    // ==========================================
    // HAMBURGER SIDEBAR DRAWER
    // ==========================================
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const closeDrawerBtn = document.getElementById('closeDrawerBtn');
    const sidebarDrawer = document.getElementById('sidebarDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerLinks = document.querySelectorAll('.drawer-link');

    function openDrawer() {
        if (sidebarDrawer) sidebarDrawer.classList.add('active');
        if (drawerOverlay) drawerOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        if (sidebarDrawer) sidebarDrawer.classList.remove('active');
        if (drawerOverlay) drawerOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (hamburgerBtn) hamburgerBtn.addEventListener('click', openDrawer);
    if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);
    drawerLinks.forEach(link => link.addEventListener('click', closeDrawer));

    // ==========================================
    // 3D TILT CARDS
    // ==========================================
    const tiltCards = document.querySelectorAll('.tilt-card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -6;
            const rotateY = ((x - centerX) / centerX) * 6;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });

    // ==========================================
    // SCROLL REVEAL
    // ==========================================
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // ==========================================
    // COUNTER ANIMATION
    // ==========================================
    const counters = document.querySelectorAll('.counter');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => counterObserver.observe(c));

    function formatNumber(num) {
        if (num >= 1000000000) return (num / 1000000000).toFixed(0) + 'B+';
        if (num >= 1000000) return (num / 1000000).toFixed(0) + 'M+';
        if (num >= 1000) return num.toLocaleString();
        return num.toString();
    }

    function animateCounter(el, target) {
        let current = 0;
        const duration = target > 10000 ? 2000 : 1200;
        const startTime = performance.now();
        function update(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 4);
            current = Math.round(ease * target);
            el.textContent = formatNumber(current);
            if (progress < 1) requestAnimationFrame(update);
            else el.textContent = formatNumber(target);
        }
        requestAnimationFrame(update);
    }

    // ==========================================
    // FOOTER WHISPER REVEAL
    // ==========================================
    const footerWhisper = document.getElementById('footerWhisper');
    if (footerWhisper) {
        const footerObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    footerWhisper.classList.add('visible');
                }
            });
        }, { threshold: 0.5 });
        footerObserver.observe(footerWhisper);
    }

    // ==========================================
    // AI CHATBOT WIDGET
    // ==========================================
    const chatToggleBtn = document.getElementById('chatToggleBtn');
    const chatToggleIcon = document.getElementById('chatToggleIcon');
    const chatWindow = document.getElementById('chatWindow');
    const chatMinimize = document.getElementById('chatMinimize');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const chatTyping = document.getElementById('chatTyping');

    let chatOpen = false;

    if (chatToggleBtn) {
        chatToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            chatOpen = !chatOpen;
            if (chatOpen) {
                chatWindow.classList.remove('hidden');
                if (chatToggleIcon) chatToggleIcon.textContent = '✕';
                if (chatInput) chatInput.focus();
            } else {
                chatWindow.classList.add('hidden');
                if (chatToggleIcon) chatToggleIcon.textContent = '💬';
            }
        });
    }

    if (chatMinimize) {
        chatMinimize.addEventListener('click', (e) => {
            e.stopPropagation();
            chatOpen = false;
            chatWindow.classList.add('hidden');
            if (chatToggleIcon) chatToggleIcon.textContent = '💬';
        });
    }

    if (chatWindow) {
        chatWindow.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${isUser ? 'user-msg' : 'bot-msg'}`;
        msgDiv.innerHTML = `
            <div class="msg-avatar">${isUser ? '👤' : '💧'}</div>
            <div class="msg-bubble">${text}</div>
        `;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        if (chatTyping) chatTyping.classList.remove('hidden');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTyping() {
        if (chatTyping) chatTyping.classList.add('hidden');
    }

    // Local knowledge base fallback
    const waterKB = {
        'ph': 'pH measures how acidic or basic water is, on a scale of 0–14. Safe drinking water typically has a pH between 6.5 and 8.5. Extreme pH can corrode pipes or indicate contamination.',
        'hardness': 'Water hardness is determined by dissolved calcium and magnesium. While hard water isn\'t a health risk, very high levels (>300 mg/L) can cause scaling and affect taste.',
        'solids': 'Total Dissolved Solids (TDS) include minerals, salts, and organic matter. WHO recommends <500 ppm for drinking water. High TDS can indicate pollution.',
        'chloramines': 'Chloramines are disinfectants used to treat drinking water. Safe levels are typically <4 ppm. They help kill bacteria but too much can cause taste/odor issues.',
        'sulfate': 'Sulfate occurs naturally in water. Levels >250 mg/L can cause a laxative effect. Our model uses sulfate as one of the 9 key potability indicators.',
        'conductivity': 'Conductivity measures water\'s ability to conduct electricity, which correlates with dissolved ions. High conductivity (>800 μS/cm) may signal contamination.',
        'organic_carbon': 'Total Organic Carbon (TOC) measures organic compounds in water. High TOC (>15 ppm) can indicate pollution and affects taste and safety.',
        'trihalomethanes': 'Trihalomethanes (THMs) are byproducts of water chlorination. The EPA limit is 80 μg/L. Long-term exposure to high THMs may increase cancer risk.',
        'turbidity': 'Turbidity measures water cloudiness. WHO recommends <1 NTU. High turbidity can harbor pathogens and indicates poor filtration.',
        'potability': 'Potability means whether water is safe to drink. Our AI model predicts this using 9 physicochemical parameters with machine learning.',
        'model': 'We evaluate 7+ ML algorithms: Logistic Regression, Decision Tree, KNN, SVM, Random Forest, Gradient Boosting, and XGBoost. The best model is selected by cross-validation ROC-AUC.',
        'xai': 'Explainable AI (XAI) makes our model transparent. We use SHAP values and feature importance plots so you can see exactly WHY the model made its prediction.',
        'shap': 'SHAP (SHapley Additive exPlanations) assigns each feature an importance value for a specific prediction. It helps explain individual predictions in our water quality model.',
        'safe': 'Safe drinking water should have: pH 6.5–8.5, TDS <500 ppm, Chloramines <4 ppm, Turbidity <1 NTU, THMs <80 μg/L. Always test before drinking from unknown sources!',
        'who': 'The World Health Organization (WHO) sets international drinking water guidelines. Our model\'s parameters are aligned with WHO water quality standards.',
        'dataset': 'Our dataset contains water quality samples with 9 features: pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, and Turbidity.',
        'hello': 'Hey there! 👋 I\'m MizuBuddy AI. Ask me anything about water quality parameters, our ML model, or how to interpret results!',
        'hi': 'Hello! 💧 I\'m here to help with water quality questions. Try asking about pH, turbidity, how our model works, or what makes water safe to drink!',
        'help': 'You can ask me about: 💧 Water parameters (pH, hardness, turbidity, etc.) 🤖 How our ML model works 🔬 SHAP / XAI explanations 🏥 WHO safety standards. Just type your question!'
    };

    function getLocalResponse(query) {
        const q = query.toLowerCase();
        for (const [key, answer] of Object.entries(waterKB)) {
            if (q.includes(key)) return answer;
        }
        if (q.includes('how') && q.includes('work')) return waterKB['model'];
        if (q.includes('drink') || q.includes('safe') || q.includes('potab')) return waterKB['safe'];
        if (q.includes('feature') || q.includes('parameter')) return waterKB['dataset'];
        if (q.includes('explain') || q.includes('interpret')) return waterKB['xai'];
        return "That's a great question! 🤔 I'm best at answering about water quality parameters (pH, hardness, turbidity, etc.), our ML model, SHAP explanations, and WHO drinking water standards. Try asking about one of those topics!";
    }

    // Action Chips Binding
    const agentChips = document.querySelectorAll('.agent-chip');
    agentChips.forEach(chip => {
        chip.addEventListener('click', (e) => {
            e.stopPropagation();
            const query = chip.getAttribute('data-query');
            if (chatInput && query) {
                chatInput.value = query;
                if (chatForm) chatForm.dispatchEvent(new Event('submit'));
            }
        });
    });

    function showAgentToast(msg) {
        let toast = document.getElementById('agentToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'agentToast';
            toast.className = 'agent-toast';
            document.body.appendChild(toast);
        }
        toast.innerHTML = `🤖 <strong>MizuAgent Live Control:</strong> ${msg}`;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3500);
    }

    function getCurrentSampleData() {
        try {
            return {
                ph: parseFloat(document.getElementById('ph')?.value || 7.0),
                Hardness: parseFloat(document.getElementById('Hardness')?.value || 180.0),
                Solids: parseFloat(document.getElementById('Solids')?.value || 15000.0),
                Chloramines: parseFloat(document.getElementById('Chloramines')?.value || 6.5),
                Sulfate: parseFloat(document.getElementById('Sulfate')?.value || 300.0),
                Conductivity: parseFloat(document.getElementById('Conductivity')?.value || 400.0),
                Organic_carbon: parseFloat(document.getElementById('Organic_carbon')?.value || 12.0),
                Trihalomethanes: parseFloat(document.getElementById('Trihalomethanes')?.value || 60.0),
                Turbidity: parseFloat(document.getElementById('Turbidity')?.value || 3.5)
            };
        } catch (err) {
            return null;
        }
    }

    function executeAgentAction(text) {
        if (!text) return;

        // 1. Fill standard demo
        if (text.includes('[ACTION:FILL_DEMO]')) {
            const demoBtn = document.getElementById('demoBtn');
            if (demoBtn) demoBtn.click();
            showAgentToast('Loaded standard sample data into form inputs.');
        }

        // 2. Run predictor model
        if (text.includes('[ACTION:RUN_PREDICTOR]')) {
            const form = document.getElementById('predictionForm');
            if (form) {
                showAgentToast('Executing machine learning prediction on active inputs...');
                setTimeout(() => form.dispatchEvent(new Event('submit')), 300);
            }
        }

        // 3. Clear form
        if (text.includes('[ACTION:CLEAR_FORM]')) {
            const form = document.getElementById('predictionForm');
            if (form) form.reset();
            showAgentToast('Cleared all form inputs.');
        }

        // 4. Set specific parameter values: [ACTION:SET_PARAM:ph=7.2,Hardness=180]
        const setParamMatch = text.match(/\[ACTION:SET_PARAM:([^\]]+)\]/);
        if (setParamMatch && setParamMatch[1]) {
            const pairs = setParamMatch[1].split(',');
            pairs.forEach(pair => {
                const [k, v] = pair.split('=');
                if (k && v) {
                    syncFieldValue(k.trim(), parseFloat(v.trim()));
                }
            });
            showAgentToast(`Updated parameter inputs: ${setParamMatch[1]}`);
        }

        // 5. Set specific values AND execute prediction: [ACTION:SET_AND_PREDICT:ph=7.2]
        const setPredictMatch = text.match(/\[ACTION:SET_AND_PREDICT:([^\]]+)\]/);
        if (setPredictMatch && setPredictMatch[1]) {
            const pairs = setPredictMatch[1].split(',');
            pairs.forEach(pair => {
                const [k, v] = pair.split('=');
                if (k && v) {
                    syncFieldValue(k.trim(), parseFloat(v.trim()));
                }
            });
            showAgentToast(`Updated parameter inputs (${setPredictMatch[1]}) & running prediction...`);
            const form = document.getElementById('predictionForm');
            if (form) setTimeout(() => form.dispatchEvent(new Event('submit')), 400);
        }

        // 6. Scroll navigation: [ACTION:SCROLL:section_id] or legacy [ACTION:SCROLL_...]
        const scrollMatch = text.match(/\[ACTION:SCROLL:([^\]]+)\]/);
        if (scrollMatch && scrollMatch[1]) {
            const secId = scrollMatch[1].trim();
            const el = document.getElementById(secId);
            if (el) {
                el.scrollIntoView({ behavior: 'smooth' });
                showAgentToast(`Navigated browser view to #${secId} section.`);
            }
        } else {
            if (text.includes('[ACTION:SCROLL_PREDICTOR]')) {
                const el = document.getElementById('predictor');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            }
            if (text.includes('[ACTION:SCROLL_PERFORMANCE]')) {
                const el = document.getElementById('performance');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }

    function formatMarkdown(text) {
        let clean = text.replace(/\[ACTION:[^\]]+\]/g, '').trim();
        clean = clean.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        clean = clean.replace(/\*(.*?)\*/g, '<em>$1</em>');
        clean = clean.replace(/\n\n/g, '<br><br>');
        clean = clean.replace(/\n/g, '<br>');
        return clean;
    }

    async function getChatResponse(userMessage) {
        try {
            const sampleData = getCurrentSampleData();
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: userMessage,
                    sample_data: sampleData
                })
            });
            if (!response.ok) throw new Error('API Error');
            const data = await response.json();
            return data.reply;
        } catch (e) {
            return getLocalResponse(userMessage);
        }
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const msg = chatInput.value.trim();
            if (!msg) return;

            addMessage(msg, true);
            chatInput.value = '';
            showTyping();

            const reply = await getChatResponse(msg);

            setTimeout(() => {
                hideTyping();
                executeAgentAction(reply);
                const formatted = formatMarkdown(reply);
                addMessage(formatted);
            }, 500);
        });
    }

    // ==========================================
    // PREDICTOR FORM
    // ==========================================
    const form = document.getElementById('predictionForm');
    const predictBtn = document.getElementById('predictBtn');
    const btnText = predictBtn ? predictBtn.querySelector('.btn-text') : null;
    const loader = predictBtn ? predictBtn.querySelector('.loader') : null;
    const demoBtn = document.getElementById('demoBtn');

    const resultPanel = document.getElementById('resultPanel');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultDesc = document.getElementById('resultDesc');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceText_el = document.getElementById('confidenceText');

    function syncFieldValue(key, value) {
        const numInput = document.getElementById(key);
        const slider = document.getElementById(key + '_slider');
        const numVal = parseFloat(value);
        if (numInput) {
            numInput.value = value;
            numInput.style.transform = 'scale(1.05)';
            numInput.style.boxShadow = '0 0 14px rgba(0, 242, 254, 0.3)';
            setTimeout(() => {
                numInput.style.transform = 'scale(1)';
                numInput.style.boxShadow = 'none';
            }, 350);
        }
        if (slider && !isNaN(numVal)) {
            slider.value = numVal;
        }
    }

    // Synchronize Range Sliders & Numerical Inputs
    const paramKeys = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'];
    paramKeys.forEach(key => {
        const numInput = document.getElementById(key);
        const slider = document.getElementById(key + '_slider');
        if (numInput && slider) {
            slider.addEventListener('input', () => {
                numInput.value = slider.value;
            });
            numInput.addEventListener('input', () => {
                if (numInput.value !== '') {
                    slider.value = numInput.value;
                }
            });
        }
    });

    const sampleData = {
        ph: 7.08,
        Hardness: 204.89,
        Solids: 20791.31,
        Chloramines: 7.30,
        Sulfate: 368.51,
        Conductivity: 564.30,
        Organic_carbon: 10.37,
        Trihalomethanes: 86.99,
        Turbidity: 2.96
    };

    // Preset Profiles Handler
    const presetProfiles = {
        well: { ph: 6.2, Hardness: 280, Solids: 18500, Chloramines: 5.5, Sulfate: 310, Conductivity: 620, Organic_carbon: 12.5, Trihalomethanes: 75, Turbidity: 3.8 },
        municipal: { ph: 7.2, Hardness: 160, Solids: 8500, Chloramines: 3.1, Sulfate: 180, Conductivity: 380, Organic_carbon: 6.5, Trihalomethanes: 35, Turbidity: 0.8 },
        river: { ph: 8.1, Hardness: 220, Solids: 24000, Chloramines: 7.8, Sulfate: 340, Conductivity: 710, Organic_carbon: 16.8, Trihalomethanes: 88, Turbidity: 5.6 },
        unsafe: { ph: 5.4, Hardness: 340, Solids: 29500, Chloramines: 9.2, Sulfate: 410, Conductivity: 950, Organic_carbon: 19.5, Trihalomethanes: 105, Turbidity: 7.8 },
        purified: { ph: 7.1, Hardness: 80, Solids: 1500, Chloramines: 0.5, Sulfate: 40, Conductivity: 120, Organic_carbon: 2.1, Trihalomethanes: 10, Turbidity: 0.3 }
    };

    const presetBtns = document.querySelectorAll('.preset-btn');
    presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const profileKey = btn.getAttribute('data-profile');
            const data = presetProfiles[profileKey];
            if (data) {
                for (const [key, value] of Object.entries(data)) {
                    syncFieldValue(key, value);
                }
                showAgentToast(`Loaded ${btn.textContent.trim()} profile.`);
            }
        });
    });

    if (demoBtn) {
        demoBtn.addEventListener('click', () => {
            for (const [key, value] of Object.entries(sampleData)) {
                syncFieldValue(key, value);
            }
            showAgentToast('Loaded standard demo sample.');
        });
    }

    let lastResultData = null;

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (btnText) btnText.classList.add('hidden');
            if (loader) loader.classList.remove('hidden');
            if (predictBtn) predictBtn.disabled = true;
            if (resultPanel) resultPanel.classList.remove('hidden');

            if (resultIcon) { resultIcon.className = 'result-icon'; resultIcon.innerHTML = '🔄'; }
            if (resultTitle) { resultTitle.textContent = 'Analyzing...'; resultTitle.className = ''; }
            if (resultDesc) resultDesc.textContent = 'Running ML classification model...';
            if (confidenceFill) confidenceFill.style.width = '0%';
            if (confidenceText_el) confidenceText_el.textContent = '0%';

            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => { data[key] = parseFloat(value); });

            try {
                const response = await fetch('http://127.0.0.1:8000/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (!response.ok) throw new Error(`API Error: ${response.status}`);

                const result = await response.json();
                lastResultData = { ...result, input_data: data };

                setTimeout(() => {
                    updateUI(result);
                }, 500);

            } catch (error) {
                console.error('Prediction failed:', error);
                if (resultIcon) { resultIcon.innerHTML = '⚠️'; resultIcon.className = 'result-icon not-potable'; }
                if (resultTitle) resultTitle.textContent = 'Error';
                if (resultDesc) resultDesc.textContent = 'Could not connect to the API. Is the FastAPI backend running?';
            } finally {
                if (btnText) btnText.classList.remove('hidden');
                if (loader) loader.classList.add('hidden');
                if (predictBtn) predictBtn.disabled = false;
            }
        });
    }

    function updateUI(result) {
        const isPotable = result.potable;
        const confidence = (result.confidence_score * 100).toFixed(1);

        if (isPotable) {
            if (resultIcon) { resultIcon.innerHTML = '💧'; resultIcon.className = 'result-icon potable'; }
            if (resultTitle) { resultTitle.textContent = 'Safe to Drink'; resultTitle.className = 'potable-text'; }
            if (resultDesc) resultDesc.textContent = 'This water sample is predicted potable and safe for consumption.';
            if (confidenceFill) confidenceFill.style.background = 'linear-gradient(90deg, #10b981, #34d399)';
        } else {
            if (resultIcon) { resultIcon.innerHTML = '☣️'; resultIcon.className = 'result-icon not-potable'; }
            if (resultTitle) { resultTitle.textContent = 'Not Potable'; resultTitle.className = 'not-potable-text'; }
            if (resultDesc) resultDesc.textContent = 'Warning: This water sample fails safety thresholds.';
            if (confidenceFill) confidenceFill.style.background = 'linear-gradient(90deg, #ef4444, #f87171)';
        }

        // Water Quality Index (WQI) Score
        const wqiScore_el = document.getElementById('wqiScore');
        const wqiFill_el = document.getElementById('wqiFill');
        const wqiStatusTag_el = document.getElementById('wqiStatusTag');
        const wqi = result.wqi || 50.0;

        if (wqiStatusTag_el) {
            if (wqi >= 80) { wqiStatusTag_el.textContent = 'EXCELLENT (SAFE)'; wqiStatusTag_el.className = 'wqi-status-tag safe'; }
            else if (wqi >= 60) { wqiStatusTag_el.textContent = 'MODERATE QUALITY'; wqiStatusTag_el.className = 'wqi-status-tag warning'; }
            else { wqiStatusTag_el.textContent = 'POOR QUALITY (UNSAFE)'; wqiStatusTag_el.className = 'wqi-status-tag danger'; }
        }

        if (wqiFill_el) {
            wqiFill_el.style.width = `${wqi}%`;
            wqiFill_el.style.background = wqi >= 70 ? 'linear-gradient(90deg, #10b981, #34d399)' : 'linear-gradient(90deg, #ef4444, #f87171)';
        }

        if (wqiScore_el) {
            wqiScore_el.textContent = wqi.toFixed(1);
        }

        // Auto-Optimize Parameters Handler
        const autoOptimizeBtn = document.getElementById('autoOptimizeBtn');
        if (autoOptimizeBtn && result.optimal_params) {
            autoOptimizeBtn.onclick = () => {
                const opt = result.optimal_params;
                for (const [key, value] of Object.entries(opt)) {
                    syncFieldValue(key, value);
                }
                showAgentToast('Optimized all 9 parameters to WHO safe targets! Re-running prediction...');
                if (form) setTimeout(() => form.dispatchEvent(new Event('submit')), 400);
            };
        }

        // Export Laboratory Analysis Report Handler
        const exportReportBtn = document.getElementById('exportReportBtn');
        if (exportReportBtn) {
            exportReportBtn.onclick = () => generateLabReportWindow(lastResultData);
        }

        // Solutions & Remediation Tips Box
        const remediationBox = document.getElementById('remediationBox');
        const remediationList = document.getElementById('remediationList');
        const askAgentFixBtn = document.getElementById('askAgentFixBtn');

        if (remediationBox && remediationList) {
            remediationList.innerHTML = '';
            const tips = result.remediation_tips || [];

            if (tips.length > 0) {
                tips.forEach(tip => {
                    const li = document.createElement('li');
                    li.innerHTML = formatMarkdown(tip);
                    remediationList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.innerHTML = isPotable 
                    ? '✅ <strong>Standard Filtration:</strong> Maintain clean carbon/sediment filters to ensure fresh taste.'
                    : '⚠️ <strong>Filtration Advice:</strong> Install a multi-stage Reverse Osmosis (RO) + UV purification system.';
                remediationList.appendChild(li);
            }

            remediationBox.className = `remediation-box ${isPotable ? 'potable-tips' : 'not-potable-tips'}`;
            remediationBox.classList.remove('hidden');
        }

        if (askAgentFixBtn) {
            askAgentFixBtn.onclick = (e) => {
                e.stopPropagation();
                if (chatWindow && chatWindow.classList.contains('hidden')) {
                    chatWindow.classList.remove('hidden');
                }
                if (chatInput) {
                    chatInput.value = isPotable
                        ? "Explain why this water sample is safe to drink according to WHO standards."
                        : "Explain why this water sample is not potable and give a step-by-step filtration solution for my parameters.";
                    if (chatForm) chatForm.dispatchEvent(new Event('submit'));
                }
            };
        }

        setTimeout(() => {
            if (confidenceFill) confidenceFill.style.width = `${confidence}%`;

            const duration = 800;
            const startTime = performance.now();

            function updateNumber(now) {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                const val = (ease * confidence).toFixed(1);
                if (confidenceText_el) confidenceText_el.textContent = `${val}%`;
                if (progress < 1) requestAnimationFrame(updateNumber);
                else if (confidenceText_el) confidenceText_el.textContent = `${confidence}%`;
            }
            requestAnimationFrame(updateNumber);
        }, 100);
    }

    function generateLabReportWindow(resData) {
        if (!resData) return;
        const inp = resData.input_data || {};
        const isPot = resData.potable;
        const conf = (resData.confidence_score * 100).toFixed(1);
        const wqi = resData.wqi || 50.0;
        const dateStr = new Date().toLocaleString();

        const reportHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Laboratory Water Quality Certificate — MizuBuddy AI</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; background: #f8fafc; color: #1e293b; }
                .cert-box { max-width: 800px; margin: 0 auto; background: #fff; border: 2px solid #0284c7; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 25px; }
                .brand { font-size: 24px; font-weight: 800; color: #0284c7; }
                .meta { text-align: right; font-size: 13px; color: #64748b; }
                .verdict-banner { padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px; font-size: 20px; font-weight: 800; }
                .verdict-potable { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
                .verdict-unsafe { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
                th, td { border: 1px solid #cbd5e1; padding: 12px 15px; text-align: left; font-size: 14px; }
                th { background: #f1f5f9; font-weight: 700; color: #334155; }
                .btn-print { background: #0284c7; color: #fff; border: none; padding: 12px 24px; border-radius: 6px; font-size: 16px; font-weight: 700; cursor: pointer; float: right; margin-top: 20px; }
                @media print { .btn-print { display: none; } }
            </style>
        </head>
        <body>
            <div class="cert-box">
                <button class="btn-print" onclick="window.print()">🖨️ Print / Save PDF</button>
                <div class="header">
                    <div class="brand">💧 MizuBuddy.AI Analysis Certificate</div>
                    <div class="meta">
                        <div>Report ID: #MZ-${Math.floor(100000 + Math.random() * 900000)}</div>
                        <div>Date: ${dateStr}</div>
                    </div>
                </div>

                <div class="verdict-banner ${isPot ? 'verdict-potable' : 'verdict-unsafe'}">
                    VERDICT: ${isPot ? 'POTABLE & SAFE FOR CONSUMPTION ✅' : 'NOT POTABLE — UNSAFE WATER SAMPLE ⚠️'}
                    <div style="font-size: 14px; font-weight: 500; margin-top: 5px;">Model Confidence: ${conf}% | Water Quality Index (WQI): ${wqi} / 100</div>
                </div>

                <h3>Measured Physicochemical Parameters vs WHO Standards</h3>
                <table>
                    <thead>
                        <tr><th>Parameter</th><th>Measured Value</th><th>WHO / EPA Standard</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>pH Level</td><td>${inp.ph || 'N/A'}</td><td>6.5 – 8.5</td><td>${(inp.ph >= 6.5 && inp.ph <= 8.5) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Hardness</td><td>${inp.Hardness || 'N/A'} mg/L</td><td>< 300 mg/L</td><td>${(inp.Hardness <= 300) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Total Dissolved Solids</td><td>${inp.Solids || 'N/A'} ppm</td><td>< 1,000 ppm</td><td>${(inp.Solids <= 1000) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Chloramines</td><td>${inp.Chloramines || 'N/A'} ppm</td><td>< 4.0 ppm</td><td>${(inp.Chloramines <= 4.0) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Sulfate</td><td>${inp.Sulfate || 'N/A'} mg/L</td><td>< 250 mg/L</td><td>${(inp.Sulfate <= 250) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Conductivity</td><td>${inp.Conductivity || 'N/A'} μS/cm</td><td>< 800 μS/cm</td><td>${(inp.Conductivity <= 800) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Organic Carbon</td><td>${inp.Organic_carbon || 'N/A'} ppm</td><td>< 10.0 ppm</td><td>${(inp.Organic_carbon <= 10) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Trihalomethanes</td><td>${inp.Trihalomethanes || 'N/A'} μg/L</td><td>< 80.0 μg/L</td><td>${(inp.Trihalomethanes <= 80) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                        <tr><td>Turbidity</td><td>${inp.Turbidity || 'N/A'} NTU</td><td>< 1.0 – 5.0 NTU</td><td>${(inp.Turbidity <= 5.0) ? 'PASS ✅' : 'FAIL ⚠️'}</td></tr>
                    </tbody>
                </table>

                <div style="font-size: 12px; color: #64748b; margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                    Certified by MizuBuddy AI Ensemble Machine Learning Classification Pipeline & WHO Guidelines.
                </div>
            </div>
        </body>
        </html>
        `;

        const win = window.open('', '_blank');
        win.document.write(reportHTML);
        win.document.close();
    }

});
