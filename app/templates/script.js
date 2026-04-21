// Elementos DOM
const queryInput = document.getElementById('queryInput');
const searchBtn = document.getElementById('searchBtn');
const tabsContainer = document.getElementById('tabsContainer');
const reasoningText = document.getElementById('reasoningText');
const sqlText = document.getElementById('sqlText');
const confidenceContent = document.getElementById('confidenceContent');
const errorBox = document.getElementById('errorBox');
const errorText = document.getElementById('errorText');
const loading = document.getElementById('loading');

// Event Listeners
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

/**
 * Alterna entre abas de resposta
 * @param {string} tabName - Nome da aba (reasoning, sql, confidence)
 */
function switchTab(tabName) {
    // Esconder todas as abas
    document.querySelectorAll('.response-container').forEach(tab => {
        tab.classList.remove('active');
    });

    // Desativar todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostrar aba selecionada
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Ativar botão
    event.target.classList.add('active');
}

/**
 * Realiza a busca na API
 */
async function performSearch() {
    const query = queryInput.value.trim();

    if (!query) {
        showError('Por favor, digite uma consulta.');
        return;
    }

    // Limpar estados anteriores
    tabsContainer.style.display = 'none';
    errorBox.classList.remove('active');
    loading.classList.add('active');
    searchBtn.disabled = true;

    try {
        const response = await fetch(`/query?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        displayResponse(data);
    } catch (error) {
        showError(`Erro ao buscar: ${error.message}`);
        console.error('Error:', error);
    } finally {
        loading.classList.remove('active');
        searchBtn.disabled = false;
        queryInput.focus();
    }
}

/**
 * Exibe a resposta do agente nas abas
 * @param {Object} data - Dados da resposta (reasoning, sql, confidence)
 */
function displayResponse(data) {
    errorBox.classList.remove('active');
    
    // Preencher campos
    reasoningText.textContent = data.reasoning || 'Não disponível';
    
    // Preencher SQL e aplicar highlight
    sqlText.textContent = data.sql || 'Não disponível';
    sqlText.classList.add('language-sql');
    
    // Remover marcação anterior de highlight
    delete sqlText.dataset.highlighted;
    
    // Aplicar highlight
    hljs.highlightElement(sqlText);
    
    // Exibir confiança com cor
    const confidenceLevel = (data.confidence || 'unknown').toLowerCase();
    const confidenceBadgeClass = `confidence-${confidenceLevel}`;
    confidenceContent.innerHTML = `
        <p><strong>Nível de Confiança:</strong></p>
        <div class="confidence-badge ${confidenceBadgeClass}">
            ${data.confidence}
        </div>
        <p style="margin-top: 16px; color: #666; font-size: 13px;">
            <strong>Significado:</strong><br>
            ${getConfidenceDescription(confidenceLevel)}
        </p>
    `;

    // Mostrar seção de resposta
    document.querySelector('.response-section').classList.add('active');
    
    // Mostrar abas
    tabsContainer.style.display = 'flex';
    
    // Resetar para primeira aba
    document.querySelectorAll('.response-container').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById('reasoning-tab').classList.add('active');
    
    document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.remove('active');
        if (idx === 0) btn.classList.add('active');
    });
}

/**
 * Retorna a descrição do nível de confiança
 * @param {string} level - Nível de confiança (high, medium, low)
 * @returns {string} Descrição do nível
 */
function getConfidenceDescription(level) {
    const descriptions = {
        'high': 'Consulta testada e verificada com confiança',
        'medium': 'Consulta não testada, resultado pode variar',
        'low': 'Consulta com incerteza, recomenda-se revisar'
    };
    return descriptions[level] || 'Nível de confiança desconhecido';
}

/**
 * Exibe mensagem de erro
 * @param {string} message - Mensagem de erro
 */
function showError(message) {
    document.querySelector('.response-section').classList.add('active');
    tabsContainer.style.display = 'none';
    errorBox.classList.add('active');
    errorText.textContent = message;
}
