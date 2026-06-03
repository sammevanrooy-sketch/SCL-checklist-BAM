<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCL Checklist Interface - BAM Wonen en Verduurzamen</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Extra custom styles voor animaties en layout */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6; /* Lichtgrijze achtergrond */
        }
        
        .sidebar-item {
            transition: all 0.2s ease-in-out;
        }
        
        .sidebar-item:hover, .sidebar-item.active {
            background-color: #008060; /* BAM groen accent */
            color: white;
            padding-left: 1.5rem; /* Schuif iets naar rechts bij hover/active */
        }

        .task-row {
            transition: background-color 0.15s ease;
            cursor: pointer;
        }

        .task-row:hover {
            background-color: #e5e7eb; /* Iets donkerder grijs bij hover over rij */
        }

        .checklist-container {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out, padding 0.3s ease-out;
            background-color: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
        }

        .checklist-container.open {
            max-height: 500px; /* Voldoende ruimte voor de checklist */
            padding: 1rem;
        }

        /* Checkbox styling */
        .custom-checkbox {
            appearance: none;
            background-color: #fff;
            margin: 0;
            font: inherit;
            color: currentColor;
            width: 1.15em;
            height: 1.15em;
            border: 1.5px solid #9ca3af;
            border-radius: 0.15em;
            display: grid;
            place-content: center;
            cursor: pointer;
            transition: all 0.1s ease-in-out;
        }

        .custom-checkbox::before {
            content: "";
            width: 0.65em;
            height: 0.65em;
            transform: scale(0);
            transition: 120ms transform ease-in-out;
            box-shadow: inset 1em 1em white;
            background-color: white;
            transform-origin: bottom left;
            clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
        }

        .custom-checkbox:checked {
            background-color: #008060;
            border-color: #008060;
        }

        .custom-checkbox:checked::before {
            transform: scale(1);
        }

        .checkbox-label {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 0.375rem;
            transition: background-color 0.2s;
        }
        
        .checkbox-label:hover {
            background-color: #f3f4f6;
        }

        .completed-text {
            text-decoration: line-through;
            color: #9ca3af;
        }
    </style>
</head>
<body class="h-screen flex overflow-hidden text-gray-800">

    <!-- Zijbalk -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col shadow-sm z-10 flex-shrink-0 hidden md:flex">
        <div class="p-6 border-b border-gray-200">
            <h1 class="text-xl font-bold text-gray-900 leading-tight">BAM Wonen & Verduurzamen</h1>
            <p class="text-sm text-gray-500 mt-1 font-medium text-[#008060]">SCL Dashboard</p>
        </div>
        
        <nav class="flex-1 overflow-y-auto py-4">
            <div class="px-4 mb-2">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Bedrijfsfases</p>
                <ul class="space-y-1">
                    <li><button onclick="loadPhase('bedrijf-1')" id="nav-bedrijf-1" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700 active">Bedrijfsfase 1</button></li>
                    <li><button onclick="loadPhase('bedrijf-2')" id="nav-bedrijf-2" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700">Bedrijfsfase 2</button></li>
                    <li><button onclick="loadPhase('bedrijf-3')" id="nav-bedrijf-3" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700">Bedrijfsfase 3</button></li>
                    <li><button onclick="loadPhase('bedrijf-4')" id="nav-bedrijf-4" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700">Bedrijfsfase 4</button></li>
                </ul>
            </div>

            <div class="px-4 mt-6">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Projectfases</p>
                <ul class="space-y-1">
                    <li><button onclick="loadPhase('project-1')" id="nav-project-1" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700">Projectfase 1</button></li>
                    <li><button onclick="loadPhase('project-2')" id="nav-project-2" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700">Projectfase 2</button></li>
                    <li><button onclick="loadPhase('project-3')" id="nav-project-3" class="sidebar-item w-full text-left px-4 py-2.5 rounded-md text-sm font-medium text-gray-700">Projectfase 3</button></li>
                </ul>
            </div>
        </nav>
    </aside>

    <!-- Hoofd content -->
    <main class="flex-1 flex flex-col overflow-hidden bg-gray-50 relative">
        
        <!-- Mobile Header (zichtbaar op kleine schermen) -->
        <header class="md:hidden bg-white border-b border-gray-200 p-4 flex justify-between items-center z-20 shadow-sm">
            <div>
                <h1 class="text-lg font-bold text-gray-900">SCL Dashboard</h1>
                <p class="text-xs text-[#008060] font-medium">BAM Wonen</p>
            </div>
            <button id="mobile-menu-btn" class="p-2 text-gray-500 hover:text-gray-700 focus:outline-none">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
        </header>

        <!-- Mobile Menu Overlay -->
        <div id="mobile-menu" class="fixed inset-0 bg-gray-800 bg-opacity-75 z-30 hidden transition-opacity">
            <div class="bg-white w-64 h-full shadow-lg flex flex-col absolute left-0 transform transition-transform -translate-x-full" id="mobile-sidebar">
                 <div class="p-4 border-b flex justify-between items-center">
                    <span class="font-bold text-lg">Menu</span>
                    <button id="close-mobile-menu" class="text-gray-500 hover:text-gray-800">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                <!-- Navigatie voor mobile (gekopieerd van desktop) -->
                <nav class="flex-1 overflow-y-auto py-4">
                    <div class="px-4 mb-2">
                        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Bedrijfsfases</p>
                        <ul class="space-y-1">
                            <li><button onclick="loadPhase('bedrijf-1'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Bedrijfsfase 1</button></li>
                            <li><button onclick="loadPhase('bedrijf-2'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Bedrijfsfase 2</button></li>
                            <li><button onclick="loadPhase('bedrijf-3'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Bedrijfsfase 3</button></li>
                            <li><button onclick="loadPhase('bedrijf-4'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Bedrijfsfase 4</button></li>
                        </ul>
                    </div>
                    <div class="px-4 mt-6">
                        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Projectfases</p>
                        <ul class="space-y-1">
                            <li><button onclick="loadPhase('project-1'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Projectfase 1</button></li>
                            <li><button onclick="loadPhase('project-2'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Projectfase 2</button></li>
                            <li><button onclick="loadPhase('project-3'); closeMobileMenu()" class="sidebar-item w-full text-left px-4 py-2 rounded-md text-sm text-gray-700">Projectfase 3</button></li>
                        </ul>
                    </div>
                </nav>
            </div>
        </div>

        <!-- Scrollable Content Area -->
        <div class="flex-1 overflow-y-auto p-4 md:p-8 w-full max-w-7xl mx-auto">
            
            <!-- Titel van de huidige sectie -->
            <div class="mb-6 pb-4 border-b border-gray-200 flex justify-between items-end">
                <div>
                    <h2 id="current-phase-title" class="text-2xl md:text-3xl font-bold text-gray-800">Bedrijfsfase 1</h2>
                    <p class="text-gray-500 text-sm mt-1">Overzicht van vereiste taken en acties voor deze trede.</p>
                </div>
                <div class="hidden sm:block">
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-blue-200">Status: In Uitvoering</span>
                </div>
            </div>

            <!-- Tabel Container -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 table-fixed">
                        <thead class="bg-gray-50">
                            <tr>
                                <th scope="col" class="w-1/12 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                <th scope="col" class="w-4/12 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Taak / Omschrijving</th>
                                <th scope="col" class="w-2/12 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Verantwoordelijke</th>
                                <th scope="col" class="w-2/12 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hoe (Middel)</th>
                                <th scope="col" class="w-2/12 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Wanneer</th>
                                <th scope="col" class="w-1/12 px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            </tr>
                        </thead>
                        <tbody id="tasks-table-body" class="bg-white divide-y divide-gray-200">
                            <!-- Inhoud wordt dynamisch geladen via JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </main>

    <script>
        // Data structuur voor de placeholders
        const dummyData = {
            'bedrijf-1': {
                title: 'Bedrijfsfase 1: Basis op orde',
                tasks: [
                    { id: 'B1.1', name: 'Opstellen veiligheidsbeleid', who: 'Directie', how: 'Document in SharePoint', when: 'Q1', 
                      checklist: [
                          'Huidige situatie analyseren', 
                          'Doelstellingen formuleren voor komend jaar', 
                          'Concept document opstellen', 
                          'Review door afdelingshoofden', 
                          'Goedkeuring en publicatie'
                      ] 
                    },
                    { id: 'B1.2', name: 'Benoemen preventiemedewerker', who: 'HR', how: 'Aanstellingsovereenkomst', when: 'Doorlopend', 
                      checklist: [
                          'Profiel opstellen', 
                          'Interne vacature uitzetten', 
                          'Selectiegesprekken voeren', 
                          'Officiële aanstelling documenteren', 
                          'Communicatie naar organisatie'
                      ] 
                    },
                    { id: 'B1.3', name: 'RI&E uitvoeren op kantoor', who: 'Preventiemedewerker', how: 'Standaard format', when: 'Jaarlijks', 
                      checklist: [
                          'Planning maken met externe adviseur', 
                          'Rondgang plannen', 
                          'Interviews afnemen', 
                          'Concept rapportage beoordelen', 
                          'Plan van Aanpak opstellen',
                          'Terugkoppeling OR'
                      ] 
                    }
                ]
            },
            'project-1': {
                title: 'Projectfase 1: Ontwerp & Voorbereiding',
                tasks: [
                    { id: 'P1.1', name: 'V&G Plan Ontwerpfase opstellen', who: 'Projectleider', how: 'V&G Template BAM', when: 'Voor start bouw', 
                      checklist: [
                          'Projectgegevens verzamelen', 
                          'Risico inventarisatie projectspecifiek', 
                          'Maatregelen bepalen', 
                          'Bijlagen toevoegen (tekeningen)', 
                          'Ondertekening door opdrachtgever'
                      ] 
                    },
                    { id: 'P1.2', name: 'Kick-off vergadering plannen', who: 'Werkvoorbereider', how: 'Teams / Fysiek', when: 'Week -2', 
                      checklist: [
                          'Agenda opstellen (V&G is vast punt)', 
                          'Onderaannemers uitnodigen', 
                          'Presentatie voorbereiden', 
                          'Presentielijst printen', 
                          'Notulen format klaarzetten'
                      ] 
                    }
                ]
            }
        };

        // Fallback data voor overige fases
        const defaultData = {
            tasks: [
                { id: 'XX.1', name: 'Placeholder Taak 1', who: 'N.n.b.', how: 'N.n.b.', when: 'TBD', 
                  checklist: ['Actiepunt 1', 'Actiepunt 2', 'Actiepunt 3', 'Actiepunt 4', 'Actiepunt 5'] 
                },
                { id: 'XX.2', name: 'Placeholder Taak 2', who: 'N.n.b.', how: 'N.n.b.', when: 'TBD', 
                  checklist: ['Actie A', 'Actie B', 'Actie C', 'Actie D', 'Actie E', 'Actie F'] 
                },
                { id: 'XX.3', name: 'Placeholder Taak 3', who: 'N.n.b.', how: 'N.n.b.', when: 'TBD', 
                  checklist: ['Controleer X', 'Valideer Y', 'Documenteer Z', 'Communiceer met team'] 
                }
            ]
        };

        // Houdt bij welke checklist momenteel open is
        let openTaskRowId = null;

        function loadPhase(phaseId) {
            // Update actieve status in sidebar
            document.querySelectorAll('.sidebar-item').forEach(item => {
                item.classList.remove('active');
            });
            // Update desktop nav
            const desktopNav = document.getElementById(`nav-${phaseId}`);
            if(desktopNav) desktopNav.classList.add('active');

            // Haal data op (of gebruik default als het nog niet bestaat)
            const phaseData = dummyData[phaseId] || { title: formatPhaseName(phaseId), tasks: defaultData.tasks };
            
            // Update titel
            document.getElementById('current-phase-title').textContent = phaseData.title;

            // Render tabel rijen
            const tbody = document.getElementById('tasks-table-body');
            tbody.innerHTML = '';
            openTaskRowId = null;

            phaseData.tasks.forEach((task, index) => {
                const rowId = `task-${phaseId}-${index}`;
                const checklistId = `checklist-${phaseId}-${index}`;

                // 1. De zichtbare tabelrij (de "strook")
                const tr = document.createElement('tr');
                tr.className = 'task-row';
                tr.id = rowId;
                tr.onclick = () => toggleChecklist(rowId, checklistId);
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${task.id}</td>
                    <td class="px-6 py-4 text-sm text-gray-800 font-medium">
                        <div class="flex items-center">
                            <span class="mr-2 text-[#008060] transition-transform duration-200" id="icon-${rowId}">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                            </span>
                            ${task.name}
                        </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${task.who}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${task.how}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${task.when}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <span id="status-${checklistId}" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            0/${task.checklist.length}
                        </span>
                    </td>
                `;

                // 2. De verborgen checklist rij
                const checklistTr = document.createElement('tr');
                checklistTr.className = 'bg-gray-50';
                
                // Genereer de HTML voor de checklist items
                let checklistHTML = '';
                task.checklist.forEach((item, itemIndex) => {
                    const checkboxId = `cb-${checklistId}-${itemIndex}`;
                    checklistHTML += `
                        <label class="checkbox-label" for="${checkboxId}">
                            <input type="checkbox" id="${checkboxId}" class="custom-checkbox mt-0.5" onchange="updateProgress('${checklistId}', ${task.checklist.length}, this)">
                            <span class="text-sm text-gray-700 select-none">${item}</span>
                        </label>
                    `;
                });

                checklistTr.innerHTML = `
                    <td colspan="6" class="p-0 border-0">
                        <div id="${checklistId}" class="checklist-container">
                            <div class="pl-14 pr-6 pb-2 pt-1">
                                <h4 class="text-sm font-semibold text-gray-900 mb-3 border-b border-gray-200 pb-2">Onderliggende acties:</h4>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2">
                                    ${checklistHTML}
                                </div>
                            </div>
                        </div>
                    </td>
                `;

                tbody.appendChild(tr);
                tbody.appendChild(checklistTr);
            });
        }

        // Helper om placeholder titels mooi te maken
        function formatPhaseName(str) {
            const parts = str.split('-');
            const type = parts[0] === 'bedrijf' ? 'Bedrijfsfase' : 'Projectfase';
            return `${type} ${parts[1]}`;
        }

        // Functie om de checklist open/dicht te klappen
        function toggleChecklist(rowId, checklistId) {
            const container = document.getElementById(checklistId);
            const icon = document.getElementById(`icon-${rowId}`);
            const row = document.getElementById(rowId);

            // Als we op een al open rij klikken, sluit deze
            if (openTaskRowId === rowId) {
                container.classList.remove('open');
                icon.style.transform = 'rotate(0deg)';
                row.style.backgroundColor = '';
                openTaskRowId = null;
                return;
            }

            // Sluit eerst de eventueel andere openstaande checklist
            if (openTaskRowId) {
                const oldChecklistId = openTaskRowId.replace('task-', 'checklist-');
                const oldContainer = document.getElementById(oldChecklistId);
                const oldIcon = document.getElementById(`icon-${openTaskRowId}`);
                const oldRow = document.getElementById(openTaskRowId);
                
                if (oldContainer) oldContainer.classList.remove('open');
                if (oldIcon) oldIcon.style.transform = 'rotate(0deg)';
                if (oldRow) oldRow.style.backgroundColor = '';
            }

            // Open de nieuwe checklist
            container.classList.add('open');
            icon.style.transform = 'rotate(90deg)';
            row.style.backgroundColor = '#f3f4f6';
            openTaskRowId = rowId;
        }

        // Functie om de voortgang van de checklist bij te werken
        function updateProgress(checklistId, totalItems, checkboxElement) {
            const container = document.getElementById(checklistId);
            const checkboxes = container.querySelectorAll('input[type="checkbox"]');
            const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
            
            // Update teller in de tabel
            const statusBadge = document.getElementById(`status-${checklistId}`);
            statusBadge.textContent = `${checkedCount}/${totalItems}`;

            // Voeg doorstreep-stijl toe aan de tekst
            const textSpan = checkboxElement.nextElementSibling;
            if(checkboxElement.checked) {
                textSpan.classList.add('completed-text');
            } else {
                textSpan.classList.remove('completed-text');
            }

            // Visuele feedback als alles is afgevinkt
            if (checkedCount === totalItems) {
                statusBadge.classList.replace('bg-gray-100', 'bg-green-100');
                statusBadge.classList.replace('text-gray-800', 'text-green-800');
            } else {
                statusBadge.classList.replace('bg-green-100', 'bg-gray-100');
                statusBadge.classList.replace('text-green-800', 'text-gray-800');
            }
        }

        // Mobile menu logica
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const closeMobileMenuBtn = document.getElementById('close-mobile-menu');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileSidebar = document.getElementById('mobile-sidebar');

        function openMobileMenu() {
            mobileMenu.classList.remove('hidden');
            // Korte delay voor de slide animatie
            setTimeout(() => {
                mobileSidebar.classList.remove('-translate-x-full');
            }, 10);
        }

        function closeMobileMenu() {
            mobileSidebar.classList.add('-translate-x-full');
            setTimeout(() => {
                mobileMenu.classList.add('hidden');
            }, 300); // Wacht tot slide animatie klaar is
        }

        mobileMenuBtn.addEventListener('click', openMobileMenu);
        closeMobileMenuBtn.addEventListener('click', closeMobileMenu);
        
        // Sluit menu als je buiten de sidebar klikt
        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) closeMobileMenu();
        });

        // Initialize: Laad de eerste fase bij het opstarten
        window.onload = () => {
            loadPhase('bedrijf-1');
        };
    </script>
</body>
</html>
