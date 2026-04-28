/* Civil Cost Manager - 메인 JavaScript */

// 프로젝트 목록 로드
async function loadProjects() {
    const container = document.getElementById('project-list');
    if (!container) return;

    try {
        const res = await fetch('/api/projects');
        const projects = await res.json();

        if (projects.length === 0) {
            container.innerHTML = '<p>등록된 프로젝트가 없습니다.</p>';
            return;
        }

        let html = '<table><thead><tr><th>프로젝트명</th><th>위치</th><th>예산</th><th>상태</th></tr></thead><tbody>';
        projects.forEach(p => {
            html += `<tr>
                <td><a href="/projects/${p.id}">${p.name}</a></td>
                <td>${p.location || '-'}</td>
                <td>${(p.budget || 0).toLocaleString()}원</td>
                <td>${p.start_date || '미정'}</td>
            </tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (err) {
        container.innerHTML = '<p>데이터를 불러오는 중 오류가 발생했습니다.</p>';
    }
}

// 프로젝트 상세 로드
async function loadProjectDetail(projectId) {
    const nameEl = document.getElementById('project-name');
    const infoEl = document.getElementById('project-info');
    const itemsEl = document.getElementById('cost-items');
    if (!nameEl) return;

    try {
        const res = await fetch(`/api/projects/${projectId}`);
        const project = await res.json();

        nameEl.textContent = project.name;
        infoEl.innerHTML = `
            <p><strong>위치:</strong> ${project.location || '-'}</p>
            <p><strong>예산:</strong> ${(project.budget || 0).toLocaleString()}원</p>
            <p><strong>기간:</strong> ${project.start_date || '미정'} ~ ${project.end_date || '미정'}</p>
        `;

        if (project.items.length === 0) {
            itemsEl.innerHTML = '<p>등록된 공사 항목이 없습니다.</p>';
            return;
        }

        let html = '<table><thead><tr><th>코드</th><th>항목명</th><th>단위</th><th>수량</th><th>단가</th><th>금액</th></tr></thead><tbody>';
        project.items.forEach(item => {
            html += `<tr>
                <td>${item.code || '-'}</td>
                <td>${item.name}</td>
                <td>${item.unit || '-'}</td>
                <td>${item.quantity || 0}</td>
                <td>${(item.unit_price || 0).toLocaleString()}</td>
                <td>${(item.total_price || 0).toLocaleString()}</td>
            </tr>`;
        });
        html += '</tbody></table>';
        itemsEl.innerHTML = html;
    } catch (err) {
        nameEl.textContent = '데이터를 불러올 수 없습니다.';
    }
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();

    if (typeof PROJECT_ID !== 'undefined') {
        loadProjectDetail(PROJECT_ID);
    }
});
