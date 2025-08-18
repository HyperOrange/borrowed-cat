// role_distribution/static/js/app.js

const { useState, useEffect } = React;

const SystemBar = () => (
    <div style={{ position: 'absolute', width: '100%', height: '49px', top: 0, left: 0, backgroundColor: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', padding: '0 1rem', fontSize: '12px', color: '#878b93' }}>
        <span style={{ marginRight: '8px' }}>9:41 AM</span>
        <img src="https://placehold.co/18x12/dedee8/212123?text=📶" alt="Mobile Signal" style={{ width: '18px', height: '12px', marginRight: '4px' }} />
        <img src="https://placehold.co/18x12/dedee8/212123?text=📶" alt="Wifi" style={{ width: '18px', height: '12px', marginRight: '4px' }} />
        <img src="https://placehold.co/24x10/dedee8/212123?text=🔋" alt="Battery" style={{ width: '24px', height: '10px' }} />
    </div>
);

const Indicator = () => (
    <div style={{ position: 'absolute', width: '100%', height: '34px', bottom: 0, left: 0, backgroundColor: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '134px', height: '5px', backgroundColor: '#ccc', borderRadius: '9999px' }}></div>
    </div>
);

const IconChevronLeft = ({ onClick }) => (
    <button
        onClick={onClick}
        style={{ position: 'absolute', left: '1.25rem', top: '0.75rem', padding: '0.5rem', borderRadius: '9999px', backgroundColor: 'transparent', border: 'none', cursor: 'pointer' }}
        aria-label="뒤로 가기"
    >
        <svg style={{ width: '24px', height: '24px', stroke: '#000' }} fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
        </svg>
    </button>
);

const App = () => {
    const [teamMembers, setTeamMembers] = useState(INITIAL_MEMBERS);
    const [currentView, setCurrentView] = useState('main');
    const [selectedMemberId, setSelectedMemberId] = useState(null);
    const [availableRoles, setAvailableRoles] = useState(INITIAL_ROLES);
    const [newRoleInput, setNewRoleInput] = useState('');
    const [selectedRolesForManual, setSelectedRolesForManual] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const totalMembers = teamMembers.length;
        const assignedMembersCount = teamMembers.filter(member => member.assigned_roles && member.assigned_roles.length > 0).length;
        if (totalMembers > 0 && assignedMembersCount === totalMembers && currentView !== 'completed') {
            setCurrentView('completed');
        } else if (assignedMembersCount < totalMembers && currentView === 'completed') {
            setCurrentView('main');
        }
    }, [teamMembers, currentView]);

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`/role-distribution/${TEAM_ID}/`);
            const data = await response.json();
            setTeamMembers(data.members);
            setAvailableRoles(data.roles);
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGoBack = () => {
        // 메인 페이지로 돌아가도록 URL을 변경
        window.location.href = `/main-page/${TEAM_ID}/`;
    };

    const handleOpenManualAssign = (memberId) => {
        const member = teamMembers.find(m => m.id === memberId);
        setSelectedMemberId(memberId);
        setSelectedRolesForManual(member?.assigned_roles || []);
        setCurrentView('manualAssign');
    };

    const handleAddRole = async () => {
        if (newRoleInput.trim() !== '') {
            try {
                const response = await fetch(`/role-distribution/${TEAM_ID}/add-role/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ role_name: newRoleInput.trim() })
                });
                const data = await response.json();
                if (response.ok) {
                    setAvailableRoles(prev => [...prev, data.role_name]);
                    setNewRoleInput('');
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error("Error adding new role:", error);
                alert("역할 추가 중 오류가 발생했습니다.");
            }
        }
    };

    const handleSelectRoleForManual = (role) => {
        setSelectedRolesForManual(prev =>
            prev.includes(role) ? prev.filter(r => r !== role) : [...prev, role]
        );
    };

    const handleManualAssignConfirm = async () => {
        if (!selectedMemberId) return;

        try {
            const response = await fetch(`/role-distribution/${TEAM_ID}/update-roles/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    member_id: selectedMemberId,
                    assigned_roles: selectedRolesForManual
                })
            });
            if (response.ok) {
                // UI 업데이트
                const updatedMembers = teamMembers.map(member =>
                    member.id === selectedMemberId ? { ...member, assigned_roles: selectedRolesForManual } : member
                );
                setTeamMembers(updatedMembers);
                setCurrentView('main');
                setSelectedMemberId(null);
                setSelectedRolesForManual([]);
            } else {
                alert("역할 할당에 실패했습니다.");
            }
        } catch (error) {
            console.error("Error assigning roles manually:", error);
            alert("역할 할당 중 오류가 발생했습니다.");
        }
    };

    const handleOpenAiAssign = () => {
        setCurrentView('aiAssign');
    };

    const handleAiAssignConfirm = async () => {
        setCurrentView('aiLoading');
        try {
            const response = await fetch(`/role-distribution/${TEAM_ID}/ai-assign/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
            });
            if (response.ok) {
                // UI 업데이트
                setTimeout(() => {
                    window.location.reload(); // 페이지 새로고침하여 최신 데이터 반영
                }, 2000);
            } else {
                alert("AI 역할 분배에 실패했습니다.");
                setCurrentView('main');
            }
        } catch (error) {
            console.error("Error with AI assignment:", error);
            alert("AI 역할 분배 중 오류가 발생했습니다.");
            setCurrentView('main');
        }
    };
    
    // CSRF 토큰을 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const handleResetRoles = async () => {
        try {
            const response = await fetch(`/role-distribution/${TEAM_ID}/update-roles/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    member_id: null,
                    assigned_roles: []
                })
            });
            if (response.ok) {
                window.location.reload();
            } else {
                alert("역할 리셋에 실패했습니다.");
            }
        } catch (error) {
            console.error("Error resetting roles:", error);
            alert("역할 리셋 중 오류가 발생했습니다.");
        }
    };

    const totalMembers = teamMembers.length;
    const assignedMembersCount = teamMembers.filter(member => member.assigned_roles && member.assigned_roles.length > 0).length;

    const renderContent = () => {
        switch (currentView) {
            case 'main':
                return (
                    <div style={{ position: 'relative', width: '100%', height: '100%', backgroundColor: '#fff', overflow: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <SystemBar />
                        <div style={{ width: '100%', height: '50px', marginTop: '49px', backgroundColor: '#fff', borderBottom: '1px solid #dee0e8', display: 'flex', alignItems: 'center', padding: '0 1rem' }}>
                            <IconChevronLeft onClick={handleGoBack} />
                            <div style={{ flexGrow: 1, textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '20px', letterSpacing: '0', lineHeight: '22px', whiteSpace: 'nowrap' }}>
                                역할 분배하기
                            </div>
                        </div>
                        <div style={{ width: 'calc(100% - 26px)', maxWidth: '382px', height: '449px', marginTop: '25px', backgroundColor: 'rgba(255, 255, 255, 0.2)', borderRadius: '20px', border: '1px solid #d9d9d9', padding: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <p style={{ marginTop: '1rem', fontWeight: '600', color: '#212123', fontSize: '20px', letterSpacing: '0', lineHeight: '24px', whiteSpace: 'nowrap' }}>
                                {totalMembers}명 중 {assignedMembersCount}명 역할분배 완료!
                            </p>
                            <div style={{ display: 'flex', flexDirection: 'column', width: '100%', marginTop: '2rem', gap: '1rem' }}>
                                {teamMembers.map(member => (
                                    <div key={member.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                                        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', height: '44px', backgroundColor: '#febf0f', borderRadius: '20px', boxShadow: '2px 2px 2px rgba(0, 0, 0, 0.1)', color: '#fff', fontWeight: '600', fontSize: '20px', whiteSpace: 'nowrap', padding: '0 1rem', marginRight: '8px' }}>
                                            {member.nickname}
                                        </div>
                                        <button onClick={() => handleOpenManualAssign(member.id)} style={{ flexShrink: 0, width: '142px', height: '44px', backgroundColor: '#ffe382', borderRadius: '20px', boxShadow: '2px 2px 2px rgba(0, 0, 0, 0.1)', color: '#fff', fontWeight: '600', fontSize: '20px', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', justifyContent: 'center', border: 'none', cursor: 'pointer' }}>+</button>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div style={{ width: 'calc(100% - 26px)', maxWidth: '382px', height: '167px', marginTop: '25px', position: 'relative' }}>
                            <div style={{ position: 'absolute', width: '100%', height: '162px', top: '5px', left: 0, backgroundColor: '#ffe382', borderRadius: '20px', overflow: 'hidden' }}>
                                <div style={{ position: 'relative', width: '166px', height: '37px', top: '69px', left: '180px' }}>
                                    <button onClick={handleOpenAiAssign} style={{ position: 'relative', width: '164px', height: '37px', backgroundColor: '#febf0f', borderRadius: '11.49px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: 'none', cursor: 'pointer' }}>
                                        <div style={{ fontWeight: '600', color: '#fff', fontSize: '15px', textAlign: 'center', lineHeight: '13.8px' }}>고양아 부탁해!</div>
                                    </button>
                                </div>
                            </div>
                            <div style={{ position: 'absolute', width: '100%', height: '35px', top: 0, left: 0, backgroundColor: '#febf0f', borderRadius: '20px 20px 0 0', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <p style={{ fontWeight: '600', color: '#fff', fontSize: '15px', textAlign: 'center', letterSpacing: '0', lineHeight: '13.8px', whiteSpace: 'nowrap' }}>
                                    빌려온 고양이 AI 추천 받기
                                </p>
                            </div>
                            <img style={{ position: 'absolute', width: '111px', height: '111px', top: '44px', left: '32px', objectFit: 'cover' }} alt="Image" src="https://placehold.co/111x111/febf0f/ffffff?text=AI" />
                        </div>
                        <Indicator />
                    </div>
                );
            case 'manualAssign':
                const memberToAssign = teamMembers.find(m => m.id === selectedMemberId);
                return (
                    <div style={{ position: 'relative', width: '100%', height: '100%', backgroundColor: '#fff', overflow: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <SystemBar />
                        <div style={{ width: '100%', height: '50px', marginTop: '49px', backgroundColor: '#fff', borderBottom: '1px solid #dee0e8', display: 'flex', alignItems: 'center', padding: '0 1rem' }}>
                            <IconChevronLeft onClick={() => setCurrentView('main')} />
                            <div style={{ flexGrow: 1, textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '20px', letterSpacing: '0', lineHeight: '22px', whiteSpace: 'nowrap' }}>
                                역할 분배하기
                            </div>
                        </div>
                        <div style={{ position: 'absolute', width: 'calc(100% - 60px)', maxWidth: '357px', height: '515px', top: '210px', backgroundColor: '#fff', borderRadius: '10px', boxShadow: '0 2px 6px rgba(0, 0, 0, 0.15)', padding: '1rem', display: 'flex', flexDirection: 'column' }}>
                            <div style={{ textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '24px', lineHeight: '22px', letterSpacing: '0', whiteSpace: 'nowrap', marginBottom: '1rem' }}>
                                팀플 역할 정하기
                            </div>
                            <div style={{ width: '100%', marginBottom: '1rem' }}>
                                <div style={{ display: 'flex', width: '100%', alignItems: 'center', gap: '10px', padding: '0 1.25rem', paddingTop: '1rem', paddingBottom: '1rem', borderRadius: '8px', overflow: 'hidden', border: '1px solid #febf0f' }}>
                                    <div style={{ position: 'relative', width: 'fit-content', fontWeight: '600', color: '#c2c4cc', fontSize: '15px', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                                        {memberToAssign?.nickname || '선택된 팀원 없음'}
                                    </div>
                                </div>
                            </div>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '1rem', flexGrow: 1, overflowY: 'auto' }}>
                                {availableRoles.map(role => (
                                    <button
                                        key={role}
                                        onClick={() => handleSelectRoleForManual(role)}
                                        style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0.75rem 1rem', borderRadius: '8px', border: '1px solid', boxShadow: '2px 2px 2px rgba(0, 0, 0, 0.1)', cursor: 'pointer',
                                            backgroundColor: selectedRolesForManual.includes(role) ? '#febf0f' : '#fff',
                                            color: selectedRolesForManual.includes(role) ? '#fff' : '#878b93',
                                            borderColor: selectedRolesForManual.includes(role) ? '#febf0f' : '#c2c4cc'
                                        }}
                                    >
                                        <div style={{ fontWeight: '600', fontSize: '15px', textAlign: 'center', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                                            {role}
                                        </div>
                                    </button>
                                ))}
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '0.75rem 1rem', borderRadius: '8px', overflow: 'hidden', border: '1px dashed #c2c4cc' }}>
                                    <input
                                        type="text"
                                        value={newRoleInput}
                                        onChange={(e) => setNewRoleInput(e.target.value)}
                                        placeholder="+ 역할 추가하기"
                                        style={{ width: '100%', textAlign: 'center', fontWeight: '600', color: '#878b93', fontSize: '15px', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap', backgroundColor: 'transparent', outline: 'none', border: 'none' }}
                                        onKeyPress={(e) => { if (e.key === 'Enter') handleAddRole(); }}
                                    />
                                    <button onClick={handleAddRole} style={{ fontWeight: '600', color: '#878b93', fontSize: '15px', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap', marginTop: '4px', border: 'none', background: 'none', cursor: 'pointer' }}>
                                        추가
                                    </button>
                                </div>
                            </div>
                            <button
                                onClick={handleManualAssignConfirm}
                                style={{ width: '100%', height: '50px', backgroundColor: '#febf0f', borderRadius: '10px', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: 'auto', border: 'none', cursor: 'pointer' }}
                            >
                                <div style={{ fontWeight: '600', color: '#fff', fontSize: '24px', textAlign: 'center', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                                    확인
                                </div>
                            </button>
                        </div>
                        <Indicator />
                    </div>
                );
            case 'aiLoading':
                return (
                    <div style={{ position: 'relative', width: '100%', height: '100%', backgroundColor: '#fff', overflow: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <SystemBar />
                        <div style={{ width: '100%', height: '50px', marginTop: '49px', backgroundColor: '#fff', borderBottom: '1px solid #dee0e8', display: 'flex', alignItems: 'center', padding: '0 1rem' }}>
                            <IconChevronLeft onClick={handleGoBack} />
                            <div style={{ flexGrow: 1, textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '20px', letterSpacing: '0', lineHeight: '22px', whiteSpace: 'nowrap' }}>
                                역할 분배하기
                            </div>
                        </div>
                        <div style={{ position: 'absolute', width: 'calc(100% - 60px)', maxWidth: '357px', height: '528px', top: '187px', backgroundColor: '#fff', borderRadius: '10px', boxShadow: '0 2px 6px rgba(0, 0, 0, 0.15)', padding: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                            <p style={{ fontWeight: '600', color: '#878b93', fontSize: '15px', textAlign: 'center', letterSpacing: '0', lineHeight: '24px', whiteSpace: 'nowrap', marginBottom: '2rem' }}>
                                고양이 AI가 열심히 맞춤역할 정하는중....
                            </p>
                            <div style={{ position: 'relative', width: '244px', height: '244px' }}>
                                <div style={{ position: 'absolute', width: '175px', height: '175px', top: '8px', left: '36px', backgroundColor: '#ffdf6b', borderRadius: '50%' }} />
                                <img
                                    style={{ position: 'absolute', width: '244px', height: '244px', top: 0, left: 0, objectFit: 'cover' }}
                                    alt="Image"
                                    src="https://placehold.co/244x244/ffdf6b/ffffff?text=AI_CAT"
                                />
                            </div>
                        </div>
                        <Indicator />
                    </div>
                );
            case 'completed':
                return (
                    <div style={{ position: 'relative', width: '100%', height: '100%', backgroundColor: '#fff', overflow: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <SystemBar />
                        <div style={{ width: '100%', height: '50px', marginTop: '49px', backgroundColor: '#fff', borderBottom: '1px solid #dee0e8', display: 'flex', alignItems: 'center', padding: '0 1rem' }}>
                            <IconChevronLeft onClick={() => setCurrentView('main')} />
                            <div style={{ flexGrow: 1, textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '20px', letterSpacing: '0', lineHeight: '22px', whiteSpace: 'nowrap' }}>
                                역할 분배하기
                            </div>
                        </div>
                        <div style={{ width: 'calc(100% - 30px)', maxWidth: '382px', height: '460px', marginTop: '25px', backgroundColor: '#fff', borderRadius: '20px', border: '1px solid #d9d9d9', padding: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <p style={{ marginTop: '1rem', fontWeight: '600', color: '#212123', fontSize: '20px', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                                {totalMembers}명 중 {assignedMembersCount}명 역할분배 완료!
                            </p>
                            <img
                                style={{ width: '85px', height: '85px', marginTop: '1rem', objectFit: 'cover' }}
                                alt="Image"
                                src="https://placehold.co/85x85/febf0f/ffffff?text=DONE"
                            />
                            <div style={{ display: 'flex', flexDirection: 'column', width: '100%', marginTop: '2rem', gap: '1rem' }}>
                                {teamMembers.map(member => (
                                    <div key={member.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                                        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', height: '44px', backgroundColor: '#febf0f', borderRadius: '20px', boxShadow: '2px 2px 2px rgba(0, 0, 0, 0.1)', color: '#fff', fontWeight: '600', fontSize: '20px', whiteSpace: 'nowrap', padding: '0 1rem', marginRight: '8px' }}>
                                            {member.nickname}
                                        </div>
                                        <div style={{ flexShrink: 0, width: '142px', height: '44px', backgroundColor: '#f39730', borderRadius: '20px', boxShadow: '2px 2px 2px rgba(0, 0, 0, 0.1)', color: '#fff', fontWeight: '600', fontSize: '20px', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', padding: '0 0.5rem' }}>
                                            {(member.assigned_roles && member.assigned_roles.length > 0)
                                                ? member.assigned_roles.join(', ')
                                                : '미정'}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <button
                            onClick={handleResetRoles}
                            style={{ width: 'calc(100% - 26px)', maxWidth: '382px', height: '50px', marginTop: '25px', backgroundColor: '#febf0f', borderRadius: '10px', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', border: 'none', cursor: 'pointer' }}
                        >
                            <div style={{ fontWeight: '600', color: '#fff', fontSize: '24px', textAlign: 'center', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                                &nbsp;&nbsp;다시 정하기
                            </div>
                        </button>
                        <button
                            onClick={() => window.location.href = `/main-page/${TEAM_ID}/`}
                            style={{ width: 'calc(100% - 26px)', maxWidth: '382px', height: '50px', marginTop: '15px', backgroundColor: '#febf0f', borderRadius: '10px', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', border: 'none', cursor: 'pointer' }}
                        >
                            <div style={{ fontWeight: '600', color: '#fff', fontSize: '24px', textAlign: 'center', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                                저장하고 나가기
                            </div>
                        </button>
                        <Indicator />
                    </div>
                );
            default:
                return null;
        }
    };
    
    return renderContent();
};

// ReactDOM.render() 호출
const rootElement = document.getElementById('root');
if (rootElement) {
    ReactDOM.render(<App />, rootElement);
}