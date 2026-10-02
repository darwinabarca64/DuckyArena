/**
 * DUCKY ARENA — COMPOSITE AVATAR ENGINE
 * Renderizador y sincronizador modular de avatares de patos 2D.
 */
window.DuckyAvatar = (function() {
    'use strict';

    const STATIC_BASE = '/static/quiz_games/avatars/';

    function createAvatarElement(avatar, options = {}) {
        const size = options.size || '54px';
        const extraClass = options.className || '';
        const id = options.id ? `id="${options.id}"` : '';
        
        const body = (avatar && avatar.body) ? avatar.body : 'body_yellow';
        const clothes = (avatar && avatar.clothes) ? avatar.clothes : '';
        const face = (avatar && avatar.face) ? avatar.face : 'face_calm';
        const head = (avatar && avatar.head) ? avatar.head : '';

        const container = document.createElement('div');
        container.className = `ducky-composite-avatar ${extraClass}`.trim();
        if (options.id) container.id = options.id;
        container.style.width = size;
        container.style.height = size;
        container.style.position = 'relative';
        container.style.display = 'inline-block';
        container.style.flexShrink = '0';

        // Capa 0: Cuerpo
        const imgBody = document.createElement('img');
        imgBody.src = `${STATIC_BASE}bodies/${body}.svg`;
        imgBody.className = 'ducky-layer ducky-layer-body';
        imgBody.alt = 'Cuerpo Pato';
        imgBody.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; object-fit: contain; pointer-events: none;';
        container.appendChild(imgBody);

        // Capa 1: Ropa
        if (clothes) {
            const imgClothes = document.createElement('img');
            imgClothes.src = `${STATIC_BASE}clothes/${clothes}.svg`;
            imgClothes.className = 'ducky-layer ducky-layer-clothes';
            imgClothes.alt = 'Ropa';
            imgClothes.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 20; object-fit: contain; pointer-events: none;';
            container.appendChild(imgClothes);
        }

        // Capa 2: Cara
        if (face) {
            const imgFace = document.createElement('img');
            imgFace.src = `${STATIC_BASE}faces/${face}.svg`;
            imgFace.className = 'ducky-layer ducky-layer-face';
            imgFace.alt = 'Expresión';
            imgFace.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 30; object-fit: contain; pointer-events: none;';
            container.appendChild(imgFace);
        }

        // Capa 3: Sombrero / Cabeza
        if (head) {
            const imgHead = document.createElement('img');
            imgHead.src = `${STATIC_BASE}heads/${head}.svg`;
            imgHead.className = 'ducky-layer ducky-layer-head';
            imgHead.alt = 'Sombrero';
            imgHead.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 40; object-fit: contain; pointer-events: none;';
            container.appendChild(imgHead);
        }

        return container;
    }

    function renderHtml(avatar, size = '54px', extraClass = '') {
        const body = (avatar && avatar.body) ? avatar.body : 'body_yellow';
        const clothes = (avatar && avatar.clothes) ? avatar.clothes : '';
        const face = (avatar && avatar.face) ? avatar.face : 'face_calm';
        const head = (avatar && avatar.head) ? avatar.head : '';

        let html = `<div class="ducky-composite-avatar ${extraClass}" style="width:${size}; height:${size}; position:relative; display:inline-block; flex-shrink:0;">`;
        html += `<img src="${STATIC_BASE}bodies/${body}.svg" alt="Cuerpo" class="ducky-layer ducky-layer-body" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:10; object-fit:contain; pointer-events:none;">`;
        if (clothes) {
            html += `<img src="${STATIC_BASE}clothes/${clothes}.svg" alt="Ropa" class="ducky-layer ducky-layer-clothes" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:20; object-fit:contain; pointer-events:none;">`;
        }
        if (face) {
            html += `<img src="${STATIC_BASE}faces/${face}.svg" alt="Cara" class="ducky-layer ducky-layer-face" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:30; object-fit:contain; pointer-events:none;">`;
        }
        if (head) {
            html += `<img src="${STATIC_BASE}heads/${head}.svg" alt="Sombrero" class="ducky-layer ducky-layer-head" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:40; object-fit:contain; pointer-events:none;">`;
        }
        html += `</div>`;
        return html;
    }

    return {
        createAvatarElement: createAvatarElement,
        renderHtml: renderHtml,
        staticBase: STATIC_BASE
    };
})();
