const { useState, useEffect, useCallback } = React;
const { initializeApp } = firebase.app;
const { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } = firebase.auth;
const { getFirestore, doc, setDoc, getDoc, onSnapshot, collection, query, updateDoc, getDocs } = firebase.firestore;

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
  const [teamMembers, setTeamMembers] = useState([]);
  const [currentView, setCurrentView] = useState('main');
  const [selectedMemberId, setSelectedMemberId] = useState(null);
  const [availableRoles, setAvailableRoles] = useState([
    "발표", "자료정리", "팀장", "발표자료 제작", "백지 피피티 제작", "보고서 작성"
  ]);
  const [newRoleInput, setNewRoleInput] = useState('');
  const [selectedRolesForManual, setSelectedRolesForManual] = useState([]);
  const [aiOptions, setAiOptions] = useState({
    target: 'unassigned',
    allowDuplicates: false,
    includedRoles: ["발표", "자료정리", "팀장", "발표자료 제작", "백지 피피티 제작", "보고서 작성"]
  });

  const [db, setDb] = useState(null);
  const [auth, setAuth] = useState(null);
  const [userId, setUserId] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);

  const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
  const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};

  useEffect(() => {
    try {
      const app = initializeApp(firebaseConfig);
      const firestore = getFirestore(app);
      const authentication = getAuth(app);
      setDb(firestore);
      setAuth(authentication);

      const unsubscribe = onAuthStateChanged(authentication, async (user) => {
        if (user) {
          setUserId(user.uid);
        } else {
          try {
            if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
              await signInWithCustomToken(authentication, __initial_auth_token);
            } else {
              await signInAnonymously(authentication);
            }
            setUserId(authentication.currentUser?.uid || crypto.randomUUID());
          } catch (error) {
            console.error("Firebase anonymous sign-in failed:", error);
            setUserId(crypto.randomUUID());
          }
        }
        setIsAuthReady(true);
      });
      return () => unsubscribe();
    } catch (error) {
      console.error("Firebase initialization failed:", error);
    }
  }, []);

  useEffect(() => {
    if (!db || !isAuthReady || !userId) return;

    const teamProjectId = 'team_project_alpha';
    const teamMembersCollectionRef = collection(db, `artifacts/${appId}/public/data/teamProjects/${teamProjectId}/members`);

    const unsubscribe = onSnapshot(teamMembersCollectionRef, (snapshot) => {
      const membersData = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setTeamMembers(membersData);

      const allAssigned = membersData.length > 0 && membersData.every(member => member.assignedRoles && member.assignedRoles.length > 0);
      if (allAssigned && currentView !== 'completed') {
        setCurrentView('completed');
      } else if (!allAssigned && currentView === 'completed') {
        setCurrentView('main');
      }
    }, (error) => {
      console.error("Error fetching team members:", error);
    });

    const addInitialMembers = async () => {
      const docRef = doc(db, `artifacts/${appId}/public/data/teamProjects/${teamProjectId}`);
      const docSnap = await getDoc(docRef);
      if (!docSnap.exists()) {
        await setDoc(docRef, { createdAt: new Date() });
      }

      const membersQuery = query(teamMembersCollectionRef);
      const existingMembers = await getDocs(membersQuery);
      if (existingMembers.empty) {
        const initialMembers = [
          { name: "동주고양", keywords: ["발표", "리더십"], assignedRoles: [] },
          { name: "기계고양", keywords: ["자료조사", "분석"], assignedRoles: [] },
          { name: "지영고양", keywords: ["보고서", "정리"], assignedRoles: [] },
          { name: "곱슬고양", keywords: ["디자인", "아이디어"], assignedRoles: [] },
        ];
        for (const member of initialMembers) {
          await setDoc(doc(teamMembersCollectionRef, crypto.randomUUID()), member);
        }
      }
    };
    addInitialMembers();

    return () => unsubscribe();
  }, [db, isAuthReady, userId, appId, currentView]);

  const handleGoBack = () => {
    setCurrentView('main');
    setSelectedMemberId(null);
    setSelectedRolesForManual([]);
  };

  const handleOpenManualAssign = (memberId) => {
    setSelectedMemberId(memberId);
    const member = teamMembers.find(m => m.id === memberId);
    setSelectedRolesForManual(member?.assignedRoles || []);
    setCurrentView('manualAssign');
  };

  const handleAddRole = () => {
    if (newRoleInput.trim() !== '' && !availableRoles.includes(newRoleInput.trim())) {
      setAvailableRoles(prev => [...prev, newRoleInput.trim()]);
      setNewRoleInput('');
    }
  };

  const handleSelectRoleForManual = (role) => {
    setSelectedRolesForManual(prev =>
      prev.includes(role) ? prev.filter(r => r !== role) : [...prev, role]
    );
  };

  const handleManualAssignConfirm = async () => {
    if (db && selectedMemberId) {
      const memberRef = doc(db, `artifacts/${appId}/public/data/teamProjects/team_project_alpha/members`, selectedMemberId);
      await updateDoc(memberRef, { assignedRoles: selectedRolesForManual });
      setCurrentView('main');
      setSelectedMemberId(null);
      setSelectedRolesForManual([]);
    }
  };

  const handleOpenAiAssign = () => {
    setCurrentView('aiAssign');
  };

  const handleAiAssignConfirm = async () => {
    setCurrentView('aiLoading');

    setTimeout(async () => {
      const membersToAssign = aiOptions.target === 'unassigned'
        ? teamMembers.filter(m => !m.assignedRoles || m.assignedRoles.length === 0)
        : teamMembers;

      let rolesPool = [...aiOptions.includedRoles];
      let assignedRolesMap = {};

      for (const member of membersToAssign) {
        let rolesForMember = [];
        if (rolesPool.length > 0) {
          if (aiOptions.allowDuplicates) {
            const numRoles = Math.floor(Math.random() * Math.min(3, rolesPool.length)) + 1;
            for (let i = 0; i < numRoles; i++) {
              rolesForMember.push(rolesPool[Math.floor(Math.random() * rolesPool.length)]);
            }
          } else {
            const availableUniqueRoles = rolesPool.filter(role => !Object.values(assignedRolesMap).flat().includes(role));
            if (availableUniqueRoles.length > 0) {
              const role = availableUniqueRoles[Math.floor(Math.random() * availableUniqueRoles.length)];
              rolesForMember.push(role);
              rolesPool = rolesPool.filter(r => r !== role);
            }
          }
        }
        assignedRolesMap[member.id] = rolesForMember;
        if (db) {
          const memberRef = doc(db, `artifacts/${appId}/public/data/teamProjects/team_project_alpha/members`, member.id);
          await updateDoc(memberRef, { assignedRoles: rolesForMember });
        }
      }
      setCurrentView('completed');
    }, 2000);
  };

  const handleResetRoles = async () => {
    if (db) {
      const teamMembersCollectionRef = collection(db, `artifacts/${appId}/public/data/teamProjects/team_project_alpha/members`);
      for (const member of teamMembers) {
        const memberRef = doc(teamMembersCollectionRef, member.id);
        await updateDoc(memberRef, { assignedRoles: [] });
      }
      setCurrentView('main');
    }
  };

  const handleSaveRoles = async () => {
    console.log("역할 분배가 저장되었습니다!");
  };

  const totalMembers = teamMembers.length;
  const assignedMembersCount = teamMembers.filter(member => member.assignedRoles && member.assignedRoles.length > 0).length;

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
                      {member.name}
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
                    <div style={{ fontWeight: '600', color: '#fff', fontSize: '15px', textAlign: 'center', letterSpacing: '0', lineHeight: '13.8px' }}>고양아 부탁해!</div>
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
              <IconChevronLeft onClick={handleGoBack} />
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
                    {memberToAssign?.name || '선택된 팀원 없음'}
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
      case 'aiAssign':
        return (
          <div style={{ position: 'relative', width: '100%', height: '100%', backgroundColor: '#fff', overflow: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <SystemBar />
            <div style={{ width: '100%', height: '50px', marginTop: '49px', backgroundColor: '#fff', borderBottom: '1px solid #dee0e8', display: 'flex', alignItems: 'center', padding: '0 1rem' }}>
              <IconChevronLeft onClick={handleGoBack} />
              <div style={{ flexGrow: 1, textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '20px', letterSpacing: '0', lineHeight: '22px', whiteSpace: 'nowrap' }}>
                역할 분배하기
              </div>
            </div>
            <div style={{ position: 'absolute', width: 'calc(100% - 60px)', maxWidth: '357px', top: '210px', backgroundColor: '#fff', borderRadius: '10px', boxShadow: '0 2px 6px rgba(0, 0, 0, 0.15)', padding: '1rem', display: 'flex', flexDirection: 'column' }}>
              <div style={{ textAlign: 'center', fontWeight: 'bold', color: '#000', fontSize: '24px', lineHeight: '22px', letterSpacing: '0', whiteSpace: 'nowrap', marginBottom: '1rem' }}>
                AI 랜덤 정하기
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <h3 style={{ fontWeight: '600', color: '#212123', fontSize: '18px', marginBottom: '8px' }}>대상 선택</h3>
                <div style={{ display: 'flex', gap: '16px' }}>
                  <button onClick={() => setAiOptions(prev => ({ ...prev, target: 'unassigned' }))} style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid', cursor: 'pointer', backgroundColor: aiOptions.target === 'unassigned' ? '#febf0f' : '#fff', color: aiOptions.target === 'unassigned' ? '#fff' : '#878b93', borderColor: aiOptions.target === 'unassigned' ? '#febf0f' : '#c2c4cc' }}>
                    역할 미정자만
                  </button>
                  <button onClick={() => setAiOptions(prev => ({ ...prev, target: 'all' }))} style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid', cursor: 'pointer', backgroundColor: aiOptions.target === 'all' ? '#febf0f' : '#fff', color: aiOptions.target === 'all' ? '#fff' : '#878b93', borderColor: aiOptions.target === 'all' ? '#febf0f' : '#c2c4cc' }}>
                    팀원 전체
                  </button>
                </div>
              </div>
              <div style={{ marginBottom: '1rem', flexGrow: 1, overflowY: 'auto' }}>
                <h3 style={{ fontWeight: '600', color: '#212123', fontSize: '18px', marginBottom: '8px' }}>포함할 역할</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  {availableRoles.map(role => (
                    <button
                      key={role}
                      onClick={() => setAiOptions(prev => ({
                        ...prev,
                        includedRoles: prev.includedRoles.includes(role)
                          ? prev.includedRoles.filter(r => r !== role)
                          : [...prev.includedRoles, role]
                      }))}
                      style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid', cursor: 'pointer', backgroundColor: aiOptions.includedRoles.includes(role) ? '#febf0f' : '#fff', color: aiOptions.includedRoles.includes(role) ? '#fff' : '#878b93', borderColor: aiOptions.includedRoles.includes(role) ? '#febf0f' : '#c2c4cc' }}>
                      {role}
                    </button>
                  ))}
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '12px 16px', borderRadius: '8px', overflow: 'hidden', border: '1px dashed #c2c4cc' }}>
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
              </div>
              <button
                onClick={handleAiAssignConfirm}
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
              <IconChevronLeft onClick={handleGoBack} />
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
                      {member.name}
                    </div>
                    <div style={{ flexShrink: 0, width: '142px', height: '44px', backgroundColor: '#f39730', borderRadius: '20px', boxShadow: '2px 2px 2px rgba(0, 0, 0, 0.1)', color: '#fff', fontWeight: '600', fontSize: '20px', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', padding: '0 0.5rem' }}>
                      {(member.assignedRoles && member.assignedRoles.length > 0)
                        ? member.assignedRoles.join(', ')
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
              onClick={handleSaveRoles}
              style={{ width: 'calc(100% - 26px)', maxWidth: '382px', height: '50px', marginTop: '15px', backgroundColor: '#febf0f', borderRadius: '10px', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', border: 'none', cursor: 'pointer' }}
            >
              <div style={{ fontWeight: '600', color: '#fff', fontSize: '24px', textAlign: 'center', lineHeight: '24px', letterSpacing: '0', whiteSpace: 'nowrap' }}>
                저장하기
              </div>
            </button>
            <Indicator />
          </div>
        );
      default:
        return null;
    }
  };
  return (
    <div style={{ width: '100%', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f5f5f5', fontFamily: 'Pretendard' }}>
      {renderContent()}
    </div>
  );
};
ReactDOM.render(<App />, document.getElementById('root'));