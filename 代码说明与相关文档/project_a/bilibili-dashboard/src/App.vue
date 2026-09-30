<template>
  <div :class="{ 'dark': isDark }" class="app-wrapper flex h-screen w-screen overflow-hidden transition-colors duration-500 bg-white dark:bg-black">

    <div class="flex h-full w-full bg-slate-50 dark:bg-[#050B14] text-slate-800 dark:text-slate-100 relative">
      
      <!-- 动态背景纹理 -->
      <div class="dot-bg absolute inset-0 pointer-events-none opacity-40 dark:opacity-20"></div>

      <!-- ================= 左侧：专业级折叠导航栏 ================= -->
      <nav class="w-20 bg-white/80 dark:bg-[#0A1128]/80 backdrop-blur-xl border-r border-slate-200 dark:border-slate-800 flex flex-col items-center py-6 shadow-lg z-20 relative">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-md shadow-blue-200 dark:shadow-[0_0_15px_rgba(59,130,246,0.3)] flex items-center justify-center text-white font-black text-2xl mb-6 cursor-pointer hover:scale-105 transition-transform">
          B
        </div>
        
        <button @click="toggleDark" class="w-10 h-10 rounded-full flex items-center justify-center mb-6 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
          <svg v-if="isDark" class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>
        
        <div class="flex flex-col gap-6 flex-1 w-full items-center">
          <div :class="['nav-item group', activeModule === 'bilibili' ? 'active' : '']" @click="switchModule('bilibili')">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            <span class="nav-tooltip">B站业务大屏</span>
          </div>
          
          <!-- 新增：多模态视觉监控 -->
          <div :class="['nav-item group', activeModule === 'multimodal' ? 'active' : '']" @click="switchModule('multimodal')">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            <span class="nav-tooltip">多模态视觉分析 (V)</span>
          </div>

          <div :class="['nav-item group', activeModule === 'monitor' ? 'active' : '']" @click="switchModule('monitor')">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2 2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path></svg>
            <span class="nav-tooltip">系统级监控中枢</span>
          </div>
          <div :class="['nav-item group', activeModule === 'ai' ? 'active' : '']" @click="activeModule = 'ai'">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            <span class="nav-tooltip">AI 助手</span>
          </div>
          
          <!-- 语音识别 -->
          <div :class="['nav-item group', activeModule === 'asr' ? 'active' : '']" @click="switchModule('asr')">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
            <span class="nav-tooltip">语音识别 (S)</span>
          </div>
        </div>

        <div class="nav-item group mt-auto">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          <span class="nav-tooltip">系统设置</span>
        </div>
      </nav>

      <!-- ================= 右侧：内容区 ================= -->
      <div class="flex-1 flex flex-col relative z-10">
        
        <!-- 顶部 Header HUD -->
        <header class="h-20 flex justify-between items-center px-8 border-b border-slate-200/60 dark:border-slate-800 bg-white/50 dark:bg-[#0A1128]/50 backdrop-blur-md">
          <div class="flex items-center gap-6">
            <h1 class="text-2xl font-black tracking-tight text-slate-800 dark:text-slate-100">
              {{ activeModule === 'ai' ? '大模型语义理解' : (activeModule === 'monitor' ? '系统核心运行监控' : (activeModule === 'multimodal' ? '多模态视觉内容检测' : '弹幕智能预警中枢')) }} 
              <span class="text-xs font-mono font-bold bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 px-2 py-1 rounded ml-2">{{ activeModule === 'ai' ? 'DEEPSEEK' : (activeModule === 'monitor' ? 'SOC' : (activeModule === 'multimodal' ? 'CV-CORE' : 'v2.5')) }}</span>
            </h1>
            
            <div class="flex gap-4 ml-6 hidden md:flex font-mono text-[11px] font-bold text-slate-500 dark:text-slate-400">
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" :class="{'shadow-[0_0_8px_#34d399]': isDark}"></span> API: ONLINE
              </div>
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 rounded-full bg-indigo-400"></span> PING: {{ Math.floor(Math.random() * 15 + 10) }}ms
              </div>
            </div>
          </div>

          <div class="flex items-center gap-5">
            <div v-if="activeModule === 'bilibili'" class="flex items-center bg-slate-100/80 dark:bg-[#050B14]/80 rounded-lg p-1 border border-slate-200 dark:border-slate-700 focus-within:border-blue-400 transition-colors shadow-inner">
              <span class="pl-3 font-mono text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">ROOM</span>
              <input v-model="targetId" class="w-28 bg-transparent text-slate-700 dark:text-slate-200 font-bold font-mono outline-none px-2 text-sm" placeholder="输入房间ID"/>
              <button @click="startPolling" class="px-4 py-1.5 bg-blue-600 text-white rounded-md text-xs font-bold hover:bg-blue-500 shadow-lg shadow-blue-200 dark:shadow-none transition-all active:scale-95 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                连接
              </button>
            </div>
            <div class="text-lg font-mono font-bold text-slate-600 dark:text-slate-400 tracking-tighter">
              {{ currentTime }}
            </div>
          </div>
        </header>

        <!-- ================= TAB 1: 业务大屏模式 (Bilibili) ================= -->
        <main class="flex-1 grid grid-cols-12 gap-6 p-6 overflow-hidden bg-transparent" v-if="activeModule === 'bilibili'">
          <!-- 左侧：AI 控制台 -->
          <section class="col-span-3 flex flex-col gap-6 min-h-0">
            <div class="tech-card flex-1 flex flex-col relative overflow-hidden">
              <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
              <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
              <div class="absolute -right-20 -top-20 w-64 h-64 rounded-full blur-[70px] opacity-40 pointer-events-none transition-colors duration-700"
                   :style="{ backgroundColor: currentAnalysis ? currentAnalysis.bully_eval.color : (isDark?'#1e3a8a':'#94a3b8') }"></div>
              <div class="flex justify-between items-center mb-6 z-10 border-b border-slate-700/50 pb-3">
                <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300">AI 智能处置终端</h2>
                <span class="font-mono text-[10px] text-slate-400 border border-slate-200 dark:border-slate-700 px-1.5 py-0.5 rounded">SYS.EVAL</span>
              </div>
              
              <div class="flex-1 flex flex-col justify-center z-10">
                <div v-if="!currentAnalysis && !isAnalyzing" class="flex flex-col items-center text-slate-400 space-y-4">
                  <div class="radar-scan"></div>
                  <p class="text-sm font-medium text-center">监听模块运行中...<br/>点击右侧弹幕截获数据</p>
                </div>
                <div v-else-if="isAnalyzing" class="flex flex-col items-center text-blue-500 space-y-4">
                  <div class="w-10 h-10 border-4 border-slate-100 dark:border-slate-700 border-t-blue-500 rounded-full animate-spin"></div>
                  <p class="text-sm font-bold font-mono animate-pulse">ANALYZING NLP DATA...</p>
                </div>
                <div v-else class="flex flex-col h-full animate-fade-in">
                  <div class="mb-4">
                    <p class="text-xs font-bold font-mono text-slate-400 mb-2">TARGET_PAYLOAD =</p>
                    <p class="text-[15px] font-medium text-slate-700 dark:text-slate-200 leading-relaxed bg-slate-50 dark:bg-[#050B14]/50 border border-slate-100 dark:border-slate-700 p-4 rounded-xl shadow-inner">
                      "{{ selectedComment }}"
                    </p>
                  </div>
                  <div class="mt-auto p-5 rounded-2xl border transition-all duration-500 relative overflow-hidden"
                       :style="{ backgroundColor: currentAnalysis.bully_eval.bgColor, borderColor: currentAnalysis.bully_eval.color + '40' }">
                    <div class="scan-line" :style="{ background: `linear-gradient(to bottom, transparent, ${currentAnalysis.bully_eval.color}40, transparent)` }"></div>
                    <div class="flex justify-between items-center mb-3">
                      <span class="text-xs font-bold font-mono tracking-wider" :style="{ color: currentAnalysis.bully_eval.color }">RISK_EVALUATION</span>
                      <span class="px-2 py-0.5 rounded text-[10px] font-black font-mono text-white shadow-sm" :style="{ backgroundColor: currentAnalysis.bully_eval.color }">LV.{{ currentAnalysis.bully_eval.level }}</span>
                    </div>
                    <div class="text-2xl font-black tracking-tight mb-2 text-slate-800 dark:text-slate-100">{{ currentAnalysis.bully_eval.levelName }}</div>
                    <div class="text-xs font-bold text-slate-500 dark:text-slate-400 mt-4">
                      ACTION: <span class="block mt-1 text-lg font-black tracking-widest" :style="{ color: currentAnalysis.bully_eval.color }">[{{ currentAnalysis.bully_eval.action }}]</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 h-28">
              <div class="tech-card flex flex-col justify-center p-5">
                <div class="text-[10px] font-bold font-mono text-slate-400 mb-1">系数</div>
                <div class="text-2xl font-black font-mono" :class="currentAnalysis && currentAnalysis.score > 0 ? 'text-emerald-500' : (currentAnalysis ? 'text-rose-500' : 'text-slate-400')">
                  {{ currentAnalysis ? currentAnalysis.score.toFixed(4) : '0.0000' }}
                </div>
              </div>
              <div class="tech-card flex flex-col justify-center p-5">
                <div class="text-[10px] font-bold font-mono text-slate-400 mb-1">FEATURE</div>
                <div class="text-lg font-black font-mono" :class="currentAnalysis && currentAnalysis.hot ? 'text-blue-500' : 'text-slate-400'">
                  {{ currentAnalysis ? (currentAnalysis.hot ? 'MATCHED' : 'NULL') : 'NULL' }}
                </div>
              </div>
            </div>
          </section>

          <!-- 中间：可视化图表 -->
          <section class="col-span-6 flex flex-col gap-6 min-h-0">
            <div class="tech-card flex-1 flex flex-col relative overflow-hidden">
              <div class="absolute -left-20 -bottom-20 w-72 h-72 rounded-full bg-emerald-100 dark:bg-emerald-900/20 blur-[80px] opacity-40 pointer-events-none"></div>
              <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300 z-10 border-b border-slate-700/50 pb-3">情感倾向比例 <span class="font-mono text-[10px] text-slate-400 ml-2">EMOTION_RATIO</span></h2>
              <div ref="pieChartRef" class="flex-1 w-full z-10"></div>
            </div>
            <div class="tech-card flex-1 flex flex-col relative overflow-hidden">
              <div class="absolute right-0 top-0 w-64 h-64 rounded-full bg-blue-50 dark:bg-blue-900/20 blur-[80px] opacity-50 pointer-events-none"></div>
              <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300 z-10 border-b border-slate-700/50 pb-3">流量趋势分析 <span class="font-mono text-[10px] text-slate-400 ml-2">TRAFFIC_TREND</span></h2>
              <div ref="lineChartRef" class="flex-1 w-full z-10 -ml-2 mt-2"></div>
            </div>
          </section>

          <!-- 右侧：实时弹幕雷达 -->
          <section class="col-span-3 tech-card flex flex-col min-h-0 relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-40 h-40 rounded-full bg-indigo-50 dark:bg-indigo-900/30 blur-[60px] opacity-60 pointer-events-none"></div>
            <div class="flex justify-between items-center mb-4 z-10 border-b border-slate-100 dark:border-slate-800 pb-2">
              <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300">实时数据雷达</h2>
              <span class="flex h-2.5 w-2.5 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
            </div>
            <div class="flex-1 overflow-y-auto pr-2 space-y-3 elegant-scrollbar z-10">
              <div v-for="(item, index) in danmakuList" :key="index" @click="analyzeComment(item.text)"
                   class="group p-4 bg-white/60 dark:bg-[#0A1128]/60 hover:bg-white dark:hover:bg-slate-800 border border-slate-100 dark:border-slate-700/50 hover:border-blue-200 dark:hover:border-blue-500/50 rounded-xl cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_4px_15px_rgb(59,130,246,0.08)] dark:hover:shadow-[0_4px_15px_rgb(59,130,246,0.15)]">
                <div class="flex justify-between items-center mb-1.5">
                  <span class="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    <div class="w-5 h-5 rounded bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center text-[10px] text-blue-600 dark:text-blue-400 font-black">{{ item.nickname.charAt(0) }}</div>
                    {{ item.nickname }}
                  </span>
                  <span class="text-[10px] font-semibold text-slate-400 font-mono">{{ item.time }}</span>
                </div>
                <div class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed pl-6 group-hover:text-slate-800 dark:group-hover:text-slate-200 transition-colors">
                  {{ item.text }}
                </div>
              </div>
            </div>
          </section>
        </main>

        <!-- ================= TAB 2: 多模态视觉监控 (Multimodal Fake) ================= -->
        <main v-if="activeModule === 'multimodal'" class="flex-1 grid grid-cols-12 gap-6 p-6 min-h-0 bg-transparent">
          
          <!-- 多模态左侧：实时图文流截获 -->
          <section class="col-span-3 tech-card flex flex-col min-h-0 relative">
            <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
            <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
            <div class="flex justify-between items-center mb-4 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h2 class="text-base font-bold tracking-wider text-slate-700 dark:text-slate-200">视觉流截获节点</h2>
              <span class="flex h-2 w-2 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
              </span>
            </div>
            
            <div class="flex-1 overflow-y-auto pr-2 space-y-4 elegant-scrollbar">
              <div v-for="(img, idx) in fakeImageList" :key="idx" @click="triggerImageScan(img)"
                   class="relative group rounded-xl overflow-hidden cursor-pointer border-2 transition-all duration-300"
                   :class="selectedImage?.id === img.id ? 'border-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.4)]' : 'border-transparent hover:border-slate-400'">
                <!-- 如果本地没有放图，这里会显示一张占位底图 -->
                <img :src="img.url" class="w-full h-32 object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                <div class="absolute bottom-0 left-0 right-0 p-2">
                  <div class="flex justify-between items-center text-[10px] font-mono">
                    <span class="text-slate-300">{{ img.time }}</span>
                    <span :class="img.isToxic ? 'text-rose-400' : 'text-emerald-400'">{{ img.isToxic ? 'High Risk' : 'Safe' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 多模态中间：全息扫描台 -->
          <section class="col-span-5 tech-card flex flex-col min-h-0 relative p-0 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-900/10 to-transparent pointer-events-none z-0"></div>
            
            <div class="p-6 pb-0 z-10 flex-none">
              <h2 class="text-base font-bold tracking-wider text-slate-700 dark:text-slate-200">深度卷积特征提取 <span class="font-mono text-[10px] text-slate-400 ml-2">CNN / OCR PROCESSOR</span></h2>
            </div>
            
            <div class="flex-1 m-6 relative rounded-xl overflow-hidden bg-[#020617] flex items-center justify-center border border-slate-700 shadow-[inset_0_0_50px_rgba(0,0,0,0.8)] z-10">
              <template v-if="selectedImage">
                <img :src="selectedImage.url" class="max-w-full max-h-full object-contain transition-all duration-300" :class="{'opacity-40 blur-[3px] grayscale': isImageScanning}" />
                
                <!-- 模拟扫描线动画 -->
                <div v-if="isImageScanning" class="absolute top-0 left-0 w-full h-[200%] bg-gradient-to-b from-transparent via-cyan-400/20 to-cyan-400/60 animate-hologram-scan pointer-events-none border-b-2 border-cyan-400 shadow-[0_5px_25px_#22d3ee]"></div>
                
                <!-- 模拟特征框 (扫描完毕后显示) -->
                <template v-if="!isImageScanning && scannedResult">
                  <!-- 识别到文字或者特征时打个框 -->
                  <div v-if="scannedResult.faceLabel" class="absolute border-2 border-rose-500 bg-rose-500/20 flex items-start justify-start p-1 shadow-[0_0_15px_#f43f5e] animate-fade-in"
                       :style="scannedResult.boxStyle">
                    <span class="text-[10px] font-mono font-bold text-white bg-rose-500 px-1.5 py-0.5">{{ scannedResult.faceLabel }}</span>
                  </div>
                  
                  <div v-if="scannedResult.ocrText" class="absolute border-2 border-cyan-400 bg-cyan-400/20 flex items-end justify-end p-1 shadow-[0_0_15px_#22d3ee] animate-fade-in"
                       :style="{ bottom: '15%', left: '10%', width: '80%', height: '25%' }">
                    <span class="text-[11px] font-mono font-bold text-white bg-cyan-500 px-1.5 py-0.5">OCR: "{{ scannedResult.ocrText }}"</span>
                  </div>
                </template>

                <!-- 旁边跳动的 Hex 数据 -->
                <div v-if="isImageScanning" class="absolute top-4 right-4 text-emerald-400 font-mono text-[10px] opacity-80 flex flex-col items-end leading-tight tracking-widest">
                  <span v-for="n in 12" :key="n">{{ hexStream[n] }}</span>
                </div>
              </template>
              <div v-else class="text-slate-500 font-mono text-sm animate-pulse tracking-widest">AWAITING VISUAL INPUT...</div>
            </div>
          </section>

          <!-- 多模态右侧：雷达图评估 -->
          <section class="col-span-4 tech-card flex flex-col min-h-0 relative">
            <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
            <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
            
            <div class="flex justify-between items-center mb-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h2 class="text-base font-bold tracking-wider text-slate-700 dark:text-slate-200">多维风险雷达</h2>
            </div>
            
            <div class="h-[60%] w-full relative">
              <!-- 当没有扫描结果时盖上一层毛玻璃 -->
              <div v-if="!scannedResult" class="absolute inset-0 z-20 backdrop-blur-sm flex items-center justify-center rounded-xl">
                 <span class="text-slate-400 font-mono text-xs bg-slate-900/80 px-3 py-1 rounded">WAITING_FOR_DATA</span>
              </div>
              <div ref="radarChartRef" class="w-full h-full"></div>
            </div>

            <!-- 分析结论 -->
            <div class="flex-1 mt-4 border-t border-slate-700/50 pt-4 flex flex-col justify-end relative">
               <div v-if="isImageScanning" class="absolute inset-0 flex items-center justify-center">
                 <div class="text-cyan-500 font-mono text-xs animate-pulse">GENERATING REPORT...</div>
               </div>
               <div v-else-if="scannedResult" class="animate-fade-in space-y-3">
                 <div v-if="scannedResult.ocrText" class="text-xs font-mono text-slate-400 mb-1">OCR_EXTRACT:</div>
                 <div v-if="scannedResult.ocrText" class="text-sm font-medium text-slate-200 bg-[#050B14]/50 p-2.5 rounded border border-slate-700 italic">"{{ scannedResult.ocrText }}"</div>
                 <div v-else class="text-xs font-mono text-slate-500 italic">No text detected in image.</div>
                 
                 <div class="flex justify-between items-center mt-4 p-3.5 rounded-lg border shadow-lg"
                      :class="scannedResult.isToxic ? 'bg-rose-500/10 border-rose-500/50 shadow-rose-500/20' : 'bg-emerald-500/10 border-emerald-500/50 shadow-emerald-500/20'">
                   <span class="font-bold tracking-wider" :class="scannedResult.isToxic ? 'text-rose-400' : 'text-emerald-400'">
                     {{ scannedResult.isToxic ? '图像高危违规' : '图像内容安全' }}
                   </span>
                   <span class="text-2xl font-black font-mono" :class="scannedResult.isToxic ? 'text-rose-500' : 'text-emerald-500'">
                     {{ scannedResult.isToxic ? 'BLOCK' : 'PASS' }}
                   </span>
                 </div>
               </div>
            </div>
          </section>

        </main>

        <!-- ================= TAB 3: 系统核心监控模式 (Monitor) ================= -->
        <main v-if="activeModule === 'monitor'" class="flex-1 flex gap-6 p-6 min-h-0 bg-transparent">
          
          <!-- 监控左侧：数据流提取 -->
          <section class="flex-[3] tech-card flex flex-col min-h-0 relative">
            <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
            <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
            
            <div class="flex justify-between items-center mb-4 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h2 class="text-base font-bold tracking-wider text-slate-700 dark:text-slate-200">实时数据流通道</h2>
              <div class="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/30 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-500/30">
                THROUGHPUT: {{ fetchSpeed }} msg/s
              </div>
            </div>
            
            <div class="flex gap-2 mb-4">
              <span @click="toggleFilterMode('all')" :class="['px-3 py-1 text-xs rounded-full font-bold cursor-pointer transition-colors', filterMode === 'all' ? 'bg-blue-100 dark:bg-blue-900/30 border border-blue-300 dark:border-blue-500/50 text-blue-600 dark:text-blue-400' : 'bg-slate-100 dark:bg-[#050B14] border border-slate-300 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800']">全量接入</span>
              <span @click="toggleFilterMode('filter')" :class="['px-3 py-1 text-xs rounded-full cursor-pointer transition-colors', filterMode === 'filter' ? 'bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-500/50 text-red-600 dark:text-red-400 font-bold' : 'bg-slate-100 dark:bg-[#050B14] border border-slate-300 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800']">异常过滤</span>
            </div>
            
            <div class="flex-1 bg-slate-50 dark:bg-[#050B14] rounded-xl border border-slate-200 dark:border-slate-700/50 p-4 overflow-y-auto elegant-scrollbar font-mono text-[11px] shadow-inner" ref="fetchStreamRef">
              <div v-for="(item, i) in fetchStream" :key="i" :class="['mb-1.5', item.isSensitive ? 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-1 rounded' : 'text-slate-600 dark:text-slate-400']">
                <span class="text-emerald-500 dark:text-emerald-400">[{{ item.time }}]</span> 
                <span :class="['font-bold ml-1', item.isSensitive ? 'text-red-500 dark:text-red-400' : 'text-blue-500 dark:text-blue-400']">
                  {{ item.isSensitive ? 'ALERT' : 'RCV' }}
                </span> <span class="opacity-50">-></span> 
                <span :class="['ml-1', item.isSensitive ? 'font-bold' : 'text-slate-700 dark:text-slate-300']">
                  {{ item.text }}
                </span>
              </div>
            </div>
          </section>

          <!-- 监控中间：分析集群状态 & 直播实时画面 -->
          <section class="flex-[4] flex flex-col gap-5 min-h-0">
             
            <!-- 核心修改：接入B站直播实时画面 -->
            <div class="flex-1 tech-card flex flex-col relative p-4">
              <h3 class="text-[11px] font-bold text-slate-500 dark:text-slate-400 font-mono absolute top-3 left-4 z-10 flex items-center gap-2 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm px-2 py-0.5 rounded shadow-sm">
                <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse shadow-[0_0_8px_#ef4444]"></span>
                LIVE_VISION_MONITOR (ROOM: {{ targetId }})
              </h3>
              <!-- 纯净原生 Video 播放层 (SOC监控级) -->
              <div class="w-full h-full mt-6 rounded-lg overflow-hidden relative bg-[#0a0a0a] shadow-[inset_0_0_30px_rgba(0,0,0,0.9)] border border-slate-200/50 dark:border-slate-700/80">
                <!-- video 必须静音才能自动播放，UI自带科技感 -->
                <video 
                  ref="liveVideoRef"
                  class="w-full h-full object-contain"
                  autoplay
                  muted>
                </video>
                <div v-if="!isPlaying" class="absolute inset-0 flex items-center justify-center text-slate-400 font-mono text-xs bg-black/60 backdrop-blur-md z-10">
                  <div class="flex flex-col items-center gap-3">
                    <div class="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    <span class="tracking-widest">AWAITING LIVE VIDEO STREAM...</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 监控右侧：代码实时处理/服务器面板 -->
          <section class="flex-[3] tech-card flex flex-col min-h-0 relative">
            <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
            <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
            
            <div class="flex justify-between items-center mb-5 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h2 class="text-base font-bold tracking-wider text-slate-700 dark:text-slate-200">内核调度终端</h2>
              <span class="text-[10px] font-mono text-slate-500 font-bold bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded">PID: 9024</span>
            </div>
            
            <div class="mb-6 space-y-4">
              <div>
                <div class="flex justify-between text-[11px] font-mono mb-1.5 font-bold"><span class="text-slate-500 dark:text-slate-400">CPU_CORE_UTILIZATION</span><span class="text-cyan-600 dark:text-cyan-400">{{ cpuUsage }}%</span></div>
                <div class="h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden shadow-inner">
                  <div class="h-full bg-gradient-to-r from-cyan-400 to-blue-500 transition-all duration-500" :style="`width: ${cpuUsage}%`"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-[11px] font-mono mb-1.5 font-bold"><span class="text-slate-500 dark:text-slate-400">MEMORY_ALLOCATION</span><span class="text-indigo-600 dark:text-indigo-400">{{ memUsage }}%</span></div>
                <div class="h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden shadow-inner">
                  <div class="h-full bg-gradient-to-r from-indigo-400 to-purple-500 transition-all duration-500" :style="`width: ${memUsage}%`"></div>
                </div>
              </div>
            </div>

            <div class="flex-1 bg-slate-50 dark:bg-[#050B14] rounded-xl border border-slate-200 dark:border-slate-700/50 p-4 overflow-y-auto elegant-scrollbar font-mono text-[11px] shadow-inner" ref="systemLogsRef">
              <div v-for="(log, i) in systemLogs" :key="i" class="mb-1.5 leading-relaxed">
                <span class="text-slate-400 dark:text-slate-500">[{{ log.time }}]</span>
                <span :class="log.type === 'ERROR' ? 'text-red-500 dark:text-red-400' : (log.type === 'WARN' ? 'text-orange-500 dark:text-orange-400' : 'text-blue-500 dark:text-blue-400')" class="font-bold ml-1">[{{ log.type }}]</span>
                <span class="text-slate-700 dark:text-slate-300 ml-1.5">{{ log.msg }}</span>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-between text-[10px] font-mono font-bold">
              <span class="text-slate-500">AVG_LATENCY: <span class="text-slate-800 dark:text-white">12ms</span></span>
              <span class="text-slate-500">WORKER_QUEUE: <span class="text-slate-800 dark:text-white">0</span></span>
            </div>
          </section>

        </main>

        <!-- ================= TAB 4: AI 助手 ================= -->
        <main class="flex-1 p-6 overflow-hidden bg-transparent" v-if="activeModule === 'ai'">
          <div class="h-full flex flex-col max-w-4xl mx-auto tech-card">
            <div class="flex justify-between items-center mb-4 p-4 border-b border-slate-200 dark:border-slate-800">
              <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300">
                AI 智能助手
                <span class="font-mono text-[10px] text-slate-400 ml-2">POWERED BY DEEPSEEK</span>
              </h2>
              <span class="flex h-2.5 w-2.5 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
            </div>
            
            <div class="flex-1 overflow-y-auto mb-4 space-y-4 p-4 elegant-scrollbar" id="chat-box">
              <div v-for="(msg, index) in chatHistory" :key="index"
                  :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
                <div :class="['max-w-[80%] rounded-2xl px-4 py-3 shadow-sm',
                            msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-[#0A1128] text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700']">
                  {{ msg.content }}
                </div>
              </div>
              <div v-if="isAiLoading" class="flex justify-start">
                <div class="bg-slate-100 dark:bg-[#0A1128] border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 animate-pulse text-slate-500 dark:text-slate-400">
                  DeepSeek 正在思考...
                </div>
              </div>
            </div>
            
            <div class="flex gap-3 pt-4 p-4 border-t border-slate-200 dark:border-slate-800">
              <input v-model="userInput" @keyup.enter="sendToAi"
                    placeholder="询问 AI 关于弹幕分析的建议..."
                    class="flex-1 bg-slate-100 dark:bg-[#050B14] border border-slate-200 dark:border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-blue-400 transition-colors dark:text-white" />
              <button @click="sendToAi" :disabled="isAiLoading"
                      class="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-xl font-bold transition-all active:scale-95 disabled:opacity-50 shadow-md shadow-blue-200 dark:shadow-none">
                发送
              </button>
            </div>
          </div>
        </main>

        <!-- ================= TAB 5: 语音识别 ================= -->
        <main class="flex-1 p-6 overflow-hidden bg-transparent" v-if="activeModule === 'asr'">
          <div class="h-full flex flex-col gap-6">
            <!-- 左侧：上传和识别 -->
            <div class="grid grid-cols-12 gap-6 flex-1">
              <section class="col-span-5 tech-card flex flex-col relative">
                <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
                <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
                <div class="absolute -left-20 -top-20 w-64 h-64 rounded-full bg-blue-100 dark:bg-blue-900/30 blur-[70px] opacity-40 pointer-events-none"></div>
                
                <div class="flex justify-between items-center mb-4 border-b border-slate-200 dark:border-slate-800 pb-3 z-10">
                  <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300">音频上传</h2>
                  <span class="flex h-2 w-2 relative">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                  </span>
                </div>
                
                <div class="flex-1 flex flex-col gap-4 z-10">
                  <div 
                    @click="triggerUpload"
                    @drop="handleDrop"
                    @dragover="handleDragOver"
                    @dragleave="handleDragLeave"
                    :class="['border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all', isDragOver ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20' : 'border-slate-300 dark:border-slate-700 hover:border-blue-400']"
                  >
                    <input type="file" ref="fileInput" @change="handleFileChange" accept=".wav,.mp3,.m4a,.flac,.aac,.ogg" class="hidden" />
                    <div v-if="!selectedFile">
                      <svg class="w-12 h-12 mx-auto text-slate-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      <p class="text-slate-600 dark:text-slate-400 font-medium">点击或拖拽上传音频文件</p>
                      <p class="text-slate-400 dark:text-slate-500 text-sm mt-2">支持 WAV, MP3, M4A, FLAC 等格式</p>
                    </div>
                    <div v-else class="text-left">
                      <div class="flex items-center gap-3 mb-3">
                        <svg class="w-10 h-10 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
                        </svg>
                        <div class="flex-1">
                          <p class="font-medium text-slate-800 dark:text-slate-200">{{ selectedFile.name }}</p>
                          <p class="text-sm text-slate-500">{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB</p>
                        </div>
                        <button @click.stop="clearFile" class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full">
                          <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <button 
                    @click="handleTranscribe" 
                    :disabled="!selectedFile || isTranscribing"
                    class="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-bold hover:from-blue-500 hover:to-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    <svg v-if="isTranscribing" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path>
                    </svg>
                    {{ isTranscribing ? '正在识别...' : '开始识别' }}
                  </button>
                </div>
              </section>
              
              <section class="col-span-7 tech-card flex flex-col relative">
                <div class="corner-bracket top-left"></div><div class="corner-bracket top-right"></div>
                <div class="corner-bracket bottom-left"></div><div class="corner-bracket bottom-right"></div>
                <div class="absolute -right-20 -top-20 w-64 h-64 rounded-full blur-[70px] opacity-40 pointer-events-none transition-colors duration-700"
                     :style="{ backgroundColor: asrAnalysis ? asrAnalysis.bully_eval.color : (isDark?'#1e3a8a':'#94a3b8') }"></div>
                
                <div class="flex justify-between items-center mb-4 border-b border-slate-200 dark:border-slate-800 pb-3 z-10">
                  <h2 class="text-base font-bold tracking-widest text-slate-700 dark:text-slate-300">识别结果</h2>
                  <span class="font-mono text-[10px] text-slate-400 border border-slate-200 dark:border-slate-700 px-1.5 py-0.5 rounded">ASR.ANALYSIS</span>
                </div>
                
                <div class="flex-1 flex flex-col gap-4 z-10 overflow-hidden">
                  <div v-if="!asrTranscript && !isTranscribing" class="flex-1 flex flex-col items-center justify-center text-slate-400">
                    <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-4l-3 3L9 16z"></path>
                    </svg>
                    <p class="text-center">上传音频文件进行识别</p>
                    <p class="text-sm text-slate-500 mt-1">识别结果将显示在这里</p>
                  </div>
                  
                  <div v-else class="flex-1 flex flex-col gap-4">
                    <div class="bg-slate-50 dark:bg-[#0A1128]/50 border border-slate-200 dark:border-slate-700 rounded-xl p-4">
                      <p class="text-xs font-bold font-mono text-slate-500 mb-2 uppercase">识别文本</p>
                      <p class="text-slate-800 dark:text-slate-200 leading-relaxed">{{ asrTranscript || '识别中...' }}</p>
                    </div>
                    
                    <div v-if="asrAnalysis" class="p-5 rounded-2xl border transition-all duration-500 relative overflow-hidden"
                         :style="{ backgroundColor: asrAnalysis.bully_eval.color + '15', borderColor: asrAnalysis.bully_eval.color + '40' }">
                      <div class="flex justify-between items-center mb-3">
                        <span class="text-xs font-bold font-mono tracking-wider" :style="{ color: asrAnalysis.bully_eval.color }">风险评估</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-black font-mono text-white shadow-sm" :style="{ backgroundColor: asrAnalysis.bully_eval.color }">LV.{{ asrAnalysis.bully_eval.level }}</span>
                      </div>
                      <div class="text-2xl font-black tracking-tight mb-2 text-slate-800 dark:text-slate-100">{{ asrAnalysis.bully_eval.levelName }}</div>
                      <div class="text-xs font-bold text-slate-500 dark:text-slate-400 mt-4">
                        处置建议: <span class="block mt-1 text-lg font-black tracking-widest" :style="{ color: asrAnalysis.bully_eval.color }">[{{ asrAnalysis.bully_eval.action }}]</span>
                      </div>
                      <div class="mt-3 flex items-center gap-2 text-xs font-mono text-slate-500">
                        <span>模型: {{ asrAnalysis.bully_eval.method }}</span>
                        <span>|</span>
                        <span>情感分数: {{ asrAnalysis.score.toFixed(4) }}</span>
                      </div>
                    </div>
                    
                    <div v-if="asrAnalysis" class="grid grid-cols-2 gap-4">
                      <div class="tech-card p-4 flex flex-col justify-center">
                        <div class="text-[10px] font-bold font-mono text-slate-500 mb-1">情感分数</div>
                        <div :class="['text-2xl font-black font-mono', asrAnalysis.score > 0 ? 'text-emerald-500' : 'text-rose-500']">
                          {{ asrAnalysis.score.toFixed(4) }}
                        </div>
                      </div>
                      <div class="tech-card p-4 flex flex-col justify-center">
                        <div class="text-[10px] font-bold font-mono text-slate-500 mb-1">特征标识</div>
                        <div :class="['text-lg font-black font-mono', asrAnalysis.hot ? 'text-blue-500' : 'text-slate-400']">
                          {{ asrAnalysis.hot ? 'MATCHED' : 'NULL' }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </main>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, shallowRef, watch, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import mpegts from 'mpegts.js'; // 核心：引入视频流解码器
import { commentCache, emotionCache, trendCache } from './utils/cache.js';
import { debounce, throttle } from './utils/debounce.js';
import { PerformanceMonitor } from './utils/performance.js';

const API_BASE = 'http://127.0.0.1:8080'

// --- 基础状态 ---
const activeModule = ref('bilibili')
const targetId = ref('6')
const isDark = ref(false)

const scaleStyle = ref({})
const currentTime = ref('')
const isAnalyzing = ref(false)

// --- 业务大屏数据 ---
const danmakuList = ref([
  { time: '12:00:00', nickname: 'SYSTEM', text: 'CONNECTION ESTABLISHED...' },
])
const currentAnalysis = ref(null)
const selectedComment = ref('')

// --- AI 数据 ---
const userInput = ref('')
const isAiLoading = ref(false)

// --- 语音识别数据 ---
const fileInput = ref(null)
const selectedFile = ref(null)
const isDragOver = ref(false)
const isTranscribing = ref(false)
const asrTranscript = ref('')
const asrAnalysis = ref(null)
const chatHistory = ref([
  { role: 'bot', content: '您好！我是 DeepSeek AI 助手。我可以帮您分析弹幕趋势，或提供网络环境维护的建议。' }
])

// --- 监控页数据 ---
const fetchStream = ref([])
const systemLogs = ref([])
const fetchSpeed = ref(0)
const cpuUsage = ref(32)
const memUsage = ref(45)
const hotWords = ref(['主播', '游戏', '技术', '前排', '哈哈哈', '房管', '封号', '什么鬼', '牛逼'])
// 异常过滤模式
const filterMode = ref('all') // 'all' 全量接入, 'filter' 异常过滤
// 敏感词列表（用于异常检测）
const sensitiveWords = ['垃圾', '废物', '傻逼', '操', '滚', '去死', '妈的', '智障', '脑瘫', '艹', '靠', 'shit', 'fuck']
// 直播流播放器状态
const liveVideoRef = ref(null);
const isPlaying = ref(false);
let flvPlayer = null;
// 初始化播放纯净视频流
const startLiveStream = async (roomId) => {
  if (!roomId) return;
  isPlaying.value = false;
  
  try {
    // 1. 请求我们自己写的 Python API，获取 B 站底层 FLV 直链
    const res = await axios.get(`http://localhost:8080/getLiveStream?roomid=${roomId}`);
    if (res.data.code === '200' && res.data.stream_url) {
      
      // 2. 如果存在旧的播放器，先销毁掉
      if (flvPlayer) {
        flvPlayer.pause();
        flvPlayer.unload();
        flvPlayer.detachMediaElement();
        flvPlayer.destroy();
        flvPlayer = null;
      }
      
      // 3. 使用 mpegts 引擎创建硬解码播放器
      if (mpegts.getFeatureList().mseLivePlayback) {
        flvPlayer = mpegts.createPlayer({
          type: 'flv',         // 格式为 flv
          isLive: true,        // 直播模式，减少延迟
          hasAudio: true,      // 解析音频
          hasVideo: true,      // 解析视频
          url: res.data.stream_url,
          cors: true           // 开启跨域允许
        });
        
        // 绑定 DOM 并播放
        if (liveVideoRef.value) {
          flvPlayer.attachMediaElement(liveVideoRef.value);
          flvPlayer.load();
          flvPlayer.play().then(() => {
            isPlaying.value = true;
          }).catch(e => console.log("浏览器限制自动播放声音，需用户交互:", e));
        }
      }
    } else {
      console.warn('获取底层视频流失败:', res.data.msg);
    }
  } catch (error) {
    console.error('API请求错误:', error);
  }
};
// 监听房间号变化，或者在点击【连接】按钮的方法里调用 startLiveStream(targetId.value)
watch(() => targetId.value, (newVal) => {
  if (activeModule.value === 'monitor' && newVal) {
    startLiveStream(newVal);
  }
});
watch(() => activeModule.value, (newVal) => {
  if (newVal === 'monitor' && targetId.value) {
    // 稍微延迟等待 DOM 渲染
    setTimeout(() => startLiveStream(targetId.value), 300);
  } else if (flvPlayer) {
    // 切走页面时销毁播放器节省性能
    flvPlayer.pause();
    flvPlayer.unload();
    flvPlayer.detachMediaElement();
    flvPlayer.destroy();
    flvPlayer = null;
    isPlaying.value = false;
  }
});

// --- 【炫技】多模态视觉计算数据 (Fake Data) ---
// 请确保在 public 目录下放入 img1.png ~ img4.png
const fakeImageList = ref([
  { id: 1, url: '/img1.png', time: '12:04:12', isToxic: true, ocr: 'CNM 你个SB NMB 素质三连', faceLabel: 'Face: Hostile (98%)', radar: [95, 20, 98, 80, 90], boxStyle: { top: '30%', left: '20%', width: '40%', height: '50%' } },
  { id: 2, url: '/img2.png', time: '12:04:25', isToxic: false, ocr: '我受不了网络暴力', faceLabel: 'Face: Sad (85%)', radar: [10, 10, 20, 15, 10], boxStyle: { top: '25%', left: '30%', width: '45%', height: '40%' } },
  { id: 3, url: '/img3.png', time: '12:05:01', isToxic: true, ocr: '操。', faceLabel: 'Face: Angry (92%)', radar: [85, 10, 95, 60, 95], boxStyle: { top: '20%', left: '20%', width: '60%', height: '50%' } },
  { id: 4, url: '/img4.png', time: '12:05:15', isToxic: true, ocr: '草了 草 草 草 草', faceLabel: null, radar: [70, 10, 85, 90, 88], boxStyle: null },
])
const selectedImage = ref(null)
const isImageScanning = ref(false)
const scannedResult = ref(null)
const hexStream = ref(Array(15).fill('00 00 00 00'))
const radarChartRef = shallowRef(null)
let radarChart = null

// --- ECharts Refs ---
const pieChartRef = shallowRef(null)
const lineChartRef = shallowRef(null)
const monitorPieChartRef = shallowRef(null)
const monitorLineChartRef = shallowRef(null)
const fetchStreamRef = shallowRef(null)
const systemLogsRef = shallowRef(null)

let pieChart, lineChart, monitorPieChart, monitorLineChart
let pollTimer = null, clockTimer = null, sysTimer = null, hexTimer = null

// --- 快捷键 & 监听 ---
const handleKeydown = (e) => {
  if (e.target.tagName === 'INPUT') return
  if (e.key.toLowerCase() === 'm') switchModule('monitor')
  if (e.key.toLowerCase() === 'd') switchModule('bilibili')
  if (e.key.toLowerCase() === 'v') switchModule('multimodal')
}

watch(activeModule, (newVal) => {
  nextTick(() => { 
    if (newVal === 'monitor') {
      // 如果图表实例不存在才初始化，否则只调用 resize
      if(!monitorPieChart || !monitorLineChart) {
        initMonitorCharts()
      } else {
        monitorPieChart.resize()
        monitorLineChart.resize()
      }
    }
    else if (newVal === 'multimodal') {
      if(!radarChart) {
        radarChart = echarts.init(radarChartRef.value)
        initRadarChart()
      } else radarChart.resize()
    }
    else if (newVal === 'bilibili') {
      // 如果图表实例不存在才初始化，否则先调用 dispose 再重新初始化
      if(!pieChart || !lineChart) {
        if (pieChartRef.value && lineChartRef.value) {
          initCharts()
        }
      } else {
        // 先销毁旧图表
        pieChart.dispose()
        lineChart.dispose()
        pieChart = null
        lineChart = null
        // 延迟一点再重新初始化，确保 DOM 已经准备好
        setTimeout(() => {
          if (pieChartRef.value && lineChartRef.value) {
            initCharts()
          }
        }, 50)
      }
    }
  })
})

watch(fetchStream, () => { nextTick(() => { if(fetchStreamRef.value) fetchStreamRef.value.scrollTop = fetchStreamRef.value.scrollHeight })}, { deep: true })
watch(systemLogs, () => { nextTick(() => { if(systemLogsRef.value) systemLogsRef.value.scrollTop = systemLogsRef.value.scrollHeight })}, { deep: true })

const pushSysLog = (type, msg) => {
  systemLogs.value.push({ time: new Date().toLocaleTimeString('zh-CN',{hour12:false}), type, msg })
  if(systemLogs.value.length > 50) systemLogs.value.shift()
}

// --- 适配与时钟 ---
const handleResize = () => {
  const designWidth = 1920
  const designHeight = 1080
  const scale = Math.min(window.innerWidth / designWidth, window.innerHeight / designHeight)
  scaleStyle.value = { transform: `scale(${scale}) translate(-50%, -50%)`, width: `${designWidth}px`, height: `${designHeight}px` }
  
  if(pieChart) pieChart.resize()
  if(lineChart) lineChart.resize()
  if(monitorPieChart) monitorPieChart.resize()
  if(monitorLineChart) monitorLineChart.resize()
  if(radarChart) radarChart.resize()
}

const updateClock = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
}

const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  updateChartsTheme()
}

const getThemeColors = () => {
  return {
    textColor: isDark.value ? '#94a3b8' : '#64748b',
    splitLine: isDark.value ? '#1e293b' : '#f1f5f9',
    pieBorder: isDark.value ? '#0F172A' : '#ffffff'
  }
}

const updateChartsTheme = () => {
  const colors = getThemeColors()
  const pOpt = { series: [{ itemStyle: { borderColor: colors.pieBorder } }], legend: { textStyle: { color: colors.textColor } } }
  const lOpt = { xAxis: { axisLabel: { color: colors.textColor } }, yAxis: { axisLabel: { color: colors.textColor }, splitLine: { lineStyle: { color: colors.splitLine } } } }
  
  if(pieChart) pieChart.setOption(pOpt)
  if(lineChart) lineChart.setOption(lOpt)
  if(monitorPieChart) monitorPieChart.setOption(pOpt)
  if(monitorLineChart) monitorLineChart.setOption(lOpt)
  if(radarChart) radarChart.setOption({ radar: { axisName: { color: colors.textColor } } })
}

// --- ECharts 初始化 ---
const initCharts = () => {
  if (!pieChartRef.value || !lineChartRef.value) return
  pieChart = echarts.init(pieChartRef.value)
  lineChart = echarts.init(lineChartRef.value)

  pieChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'rgba(15,23,42,0.95)', textStyle: { color: '#f8fafc', fontWeight: 'bold' }, borderWidth: 0, extraCssText: 'border-radius: 8px;' },
    legend: { bottom: '0%', icon: 'circle', itemWidth: 8, textStyle: { color: '#64748b', fontWeight: '600' } },
    color: ['#34d399', '#fb7185'],
    series: [{
      name: '情感分布', type: 'pie', radius: ['50%', '75%'], center: ['50%', '45%'],
      itemStyle: { borderColor: isDark.value ? '#0F172A' : '#ffffff', borderWidth: 4, borderRadius: 8 },
      label: { show: false },
      data: [{ value: 65, name: '正面倾向' }, { value: 35, name: '负面倾向' }]
    }]
  })

  lineChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(15,23,42,0.95)', textStyle: { color: '#f8fafc', fontWeight: 'bold' }, borderWidth: 0, extraCssText: 'border-radius: 8px;' },
    grid: { left: '2%', right: '2%', bottom: '0%', top: '10%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: ['12:00', '12:01', '12:02', '12:03'], axisLabel: { color: '#94a3b8', margin: 12, fontWeight: '600', fontFamily: 'monospace' }, axisLine: { show: false }, axisTick: { show: false } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: isDark.value ? '#1e293b' : '#f1f5f9', type: 'dashed' } }, axisLabel: { color: '#94a3b8', fontFamily: 'monospace' } },
    series: [{
      data: [10, 22, 15, 30], type: 'line', smooth: 0.4, showSymbol: false, symbolSize: 8,
      itemStyle: { color: '#60a5fa', borderWidth: 2, borderColor: '#fff' },
      lineStyle: { width: 3, color: '#60a5fa' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(96, 165, 250, 0.2)' }, { offset: 1, color: 'rgba(96, 165, 250, 0)' }]) }
    }]
  })
}

const initMonitorCharts = () => {
  if (!monitorPieChartRef.value || !monitorLineChartRef.value) return
  monitorPieChart = echarts.init(monitorPieChartRef.value)
  monitorLineChart = echarts.init(monitorLineChartRef.value)
  const colors = getThemeColors()

  monitorPieChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'rgba(15,23,42,0.9)', textStyle: {color:'#f8fafc'}, borderColor: '#334155' },
    legend: { show: false },
    color: ['#3b82f6', '#eab308', '#ef4444', '#10b981'],
    series: [{
      type: 'pie', radius: ['50%', '80%'], center: ['50%', '50%'],
      itemStyle: { borderColor: colors.pieBorder, borderWidth: 3, borderRadius: 5 },
      label: { show: false },
      data: [{value:420, name:'LV.0 正常'}, {value:120, name:'LV.1 轻微'},{value:45, name:'LV.2 敏感'},{value:12, name:'LV.3 高危'}]
    }]
  })

  monitorLineChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(15,23,42,0.9)', textStyle: {color:'#f8fafc'}, borderColor: '#334155' },
    grid: { left: '2%', right: '3%', bottom: '5%', top: '15%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: ['-5m','-4m','-3m','-2m','-1m','now'], axisLabel: { color: colors.textColor, fontFamily: 'monospace' }, axisLine: { show: false }, axisTick: { show: false } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: colors.splitLine, type: 'dashed' } }, axisLabel: { color: colors.textColor } },
    series: [{
      data: [2, 5, 1, 8, 3, 6], type: 'line', smooth: 0.3, showSymbol: false,
      itemStyle: { color: '#f43f5e' }, lineStyle: { width: 2, color: '#f43f5e' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(244,63,94,0.2)' }, { offset: 1, color: 'rgba(244,63,94,0)' }]) }
    }]
  })
}

// 初始化雷达图
const initRadarChart = () => {
  if (!radarChartRef.value) return
  const colors = getThemeColors()
  radarChart.setOption({
    tooltip: { backgroundColor: 'rgba(15,23,42,0.9)', textStyle: {color:'#f8fafc'}, borderColor: '#334155' },
    radar: {
      indicator: [
        { name: '涉黄(Porn)', max: 100 },
        { name: '暴恐(Violent)', max: 100 },
        { name: '侮辱(Insult)', max: 100 },
        { name: '讽刺(Sarcasm)', max: 100 },
        { name: '低俗(Vulgar)', max: 100 }
      ],
      axisName: { color: colors.textColor, fontWeight: 'bold' },
      splitArea: { areaStyle: { color: ['rgba(59, 130, 246, 0.05)', 'rgba(59, 130, 246, 0.1)'] } },
      axisLine: { lineStyle: { color: 'rgba(59, 130, 246, 0.2)' } },
      splitLine: { lineStyle: { color: 'rgba(59, 130, 246, 0.2)' } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [0, 0, 0, 0, 0], name: '视觉多维风险特征',
        itemStyle: { color: '#06b6d4' },
        areaStyle: { color: 'rgba(6, 182, 212, 0.4)' }
      }]
    }]
  })
}

// --- 数据获取与业务 ---
const fetchBulletScreen = async () => { 
  try { 
    pushSysLog('INFO', `Fetching stream from Room [${targetId.value}]...`)
    await axios.get(`${API_BASE}/getBulletScreen`, { params: { roomid: targetId.value }}) 
  } catch (err) {
    pushSysLog('WARN', `Ratelimit triggered or network delay.`)
  } 
}

// 创建性能监控实例
const performanceMonitor = new PerformanceMonitor();

const fetchData = async () => {
  performanceMonitor.startMetric('fetchData');
  try {
    const currentKey = targetId.value
    
    // 先检查情感分析缓存
    if (emotionCache.has(currentKey)) {
      const cachedEmotion = emotionCache.get(currentKey);
      if (pieChart && activeModule.value === 'bilibili') {
        pieChart.setOption({ series: [{ data: [{ value: cachedEmotion.positive, name: '正面倾向' }, { value: cachedEmotion.negative, name: '负面倾向' }] }] });
      }
      if (monitorPieChart && activeModule.value === 'monitor') {
        monitorPieChart.setOption({ series: [{ data: [{value:420, name:'LV.0 正常'}, {value:120, name:'LV.1 轻微'},{value:45, name:'LV.2 敏感'},{value:12, name:'LV.3 高危'}] }] });
      }
    } else {
      const emotionRes = await axios.get(`${API_BASE}/EmotionAnalysis`, { params: { roomid: currentKey }})
      if(emotionRes.data && emotionRes.data.d2) {
        const emotionData = { positive: emotionRes.data.d2[0], negative: emotionRes.data.d2[1] };
        emotionCache.set(currentKey, emotionData);
        if (pieChart && activeModule.value === 'bilibili') {
          pieChart.setOption({ series: [{ data: [{ value: emotionRes.data.d2[0], name: '正面倾向' }, { value: emotionRes.data.d2[1], name: '负面倾向' }] }] });
        }
        if (monitorPieChart && activeModule.value === 'monitor') {
          monitorPieChart.setOption({ series: [{ data: [{value:420, name:'LV.0 正常'}, {value:120, name:'LV.1 轻微'},{value:45, name:'LV.2 敏感'},{value:12, name:'LV.3 高危'}] }] });
        }
      }
    }

    // 先检查趋势分析缓存
    if (trendCache.has(currentKey)) {
      const cachedTrend = trendCache.get(currentKey);
      if (lineChart && activeModule.value === 'bilibili') {
        lineChart.setOption({ xAxis: { data: cachedTrend.name }, series: [{ data: cachedTrend.value }] });
      }
      if (monitorLineChart && activeModule.value === 'monitor') {
        monitorLineChart.setOption({ xAxis: { data: cachedTrend.name }, series: [{ data: cachedTrend.value }] });
      }
    } else {
      const trendRes = await axios.get(`${API_BASE}/TimeRelatedAnalysis`, { params: { roomid: currentKey }})
      if(trendRes.data && trendRes.data.name) {
        trendCache.set(currentKey, trendRes.data);
        if (lineChart && activeModule.value === 'bilibili') {
          lineChart.setOption({ xAxis: { data: trendRes.data.name }, series: [{ data: trendRes.data.value }] });
        }
        if (monitorLineChart && activeModule.value === 'monitor') {
          monitorLineChart.setOption({ xAxis: { data: trendRes.data.name }, series: [{ data: trendRes.data.value }] });
        }
      }
    }

    const listRes = await axios.get(`${API_BASE}/alldata`, { params: { roomid: currentKey }})
    if(listRes.data && listRes.data.d2 && listRes.data.d2.length > 0) {
      
      fetchSpeed.value = Math.floor(Math.random() * 12 + 3)
      const newItems = listRes.data.d2.map(item => {
        const parts = item.split('*')
        return { time: parts[0]||'', nickname: parts[1]||'User', text: parts[2]||item }
      }).reverse()
      
      // 更新首页弹幕列表
      if (activeModule.value === 'bilibili') {
        danmakuList.value = newItems
      }

      // 推入监控页流（根据过滤模式）
      newItems.slice(0, 3).forEach(i => {
        if(filterMode.value === 'all' || containsSensitiveWord(i.text)) {
          fetchStream.value.push({ 
            time: i.time.split(' ')[1]||'', 
            text: i.text,
            isSensitive: containsSensitiveWord(i.text)
          })
          if(fetchStream.value.length > 50) fetchStream.value.shift()
        }
      })
      pushSysLog('INFO', `Extracted ${newItems.length} records.`)
    }
  } catch (err) {
    pushSysLog('ERROR', `Data pipeline sync failed: ${err.message}`)
  } finally {
    performanceMonitor.endMetric('fetchData');
    const duration = performanceMonitor.getMetric('fetchData')?.duration;
    if (duration) {
      pushSysLog('INFO', `Data pipeline completed in ${duration.toFixed(2)}ms`);
    }
  }
}


const getEvalByScore = (score) => {
  let evalData = { level: 0, levelName: "正常放行", action: "PASS", color: "#10b981", bgColor: "rgba(16, 185, 129, 0.05)" }
  if(score < -0.8) evalData = { level: 4, levelName: "高危欺凌", action: "BLOCK & REPORT", color: "#f43f5e", bgColor: "rgba(244, 63, 94, 0.08)" }
  else if(score < -0.5) evalData = { level: 3, levelName: "重度违规", action: "BLOCK", color: "#f97316", bgColor: "rgba(249, 115, 22, 0.08)" }
  else if(score < -0.2) evalData = { level: 2, levelName: "中度风险", action: "WARN", color: "#eab308", bgColor: "rgba(234, 179, 8, 0.08)" }
  else if(score < 0) evalData = { level: 1, levelName: "轻度负面", action: "NOTICE", color: "#3b82f6", bgColor: "rgba(59, 130, 246, 0.08)" }
  return evalData
}

const analyzeComment = async (text) => {
  selectedComment.value = text
  isAnalyzing.value = true
  currentAnalysis.value = null
  pushSysLog('INFO', `Submit NLP task: "${text.substring(0,8)}..."`)
  
  // 先检查缓存
  if (commentCache.has(text)) {
    const cachedData = commentCache.get(text)
    currentAnalysis.value = cachedData
    pushSysLog('INFO', `NLP resolved from cache. Score: ${cachedData.score.toFixed(3)}`)
    isAnalyzing.value = false
    return
  }
  
  try {
    const res = await axios.get(`${API_BASE}/CommentAnalysis`, { params: { sentence: text }, timeout: 3000 })
    let data = res.data
    if (!data.bully_eval) {
       let score = data.score || (Math.random() * 2 - 1)
       data.bully_eval = getEvalByScore(score)
    } else {
        data.bully_eval.bgColor = data.bully_eval.color + '15' 
    }
    data.isMock = false
    currentAnalysis.value = data
    // 将结果存入缓存
    commentCache.set(text, data)
    pushSysLog('INFO', `NLP resolved. Score: ${data.score.toFixed(3)}`)
  } catch (err) {
    pushSysLog('WARN', `NLP timeout, using local heuristic fallback.`)
    let mockScore = 0.5;
    if (text.includes('死') || text.includes('滚') || text.includes('垃圾') || text.includes('恶心') || text.includes('傻')) {
        mockScore = - (Math.random() * 0.5 + 0.5);
    } else {
        mockScore = Math.random() * 0.5 + 0.2; 
    }
    const mockData = { score: mockScore, hot: mockScore < 0 ? true : false, isMock: true, bully_eval: getEvalByScore(mockScore) }
    currentAnalysis.value = mockData
    // 将模拟结果也存入缓存
    commentCache.set(text, mockData)
  } finally {
    isAnalyzing.value = false
  }
}

// --- 多模态视觉扫描特效 (FAKE) ---
const triggerImageScan = (img) => {
  selectedImage.value = img
  isImageScanning.value = true
  scannedResult.value = null
  
  // 生成随机 Hex 流
  if(hexTimer) clearInterval(hexTimer)
  hexTimer = setInterval(() => {
    hexStream.value = Array(15).fill(0).map(() => Array(4).fill(0).map(() => Math.floor(Math.random()*256).toString(16).padStart(2,'0').toUpperCase()).join(' '))
  }, 100)

  // 1.5s 后停止扫描出结果
  setTimeout(() => {
    isImageScanning.value = false
    clearInterval(hexTimer)
    scannedResult.value = { isToxic: img.isToxic, ocrText: img.ocr, faceLabel: img.faceLabel, boxStyle: img.boxStyle }
    
    // 更新雷达图
    if(radarChart) {
      radarChart.setOption({
        series: [{
          data: [{
            value: img.radar, name: '视觉多维风险特征',
            itemStyle: { color: img.isToxic ? '#f43f5e' : '#06b6d4' },
            areaStyle: { color: img.isToxic ? 'rgba(244, 63, 94, 0.4)' : 'rgba(6, 182, 212, 0.4)' }
          }]
        }]
      })
    }
  }, 1500)
}

const startPolling = () => {
  if(pollTimer) clearInterval(pollTimer)
  pushSysLog('INFO', 'Initializing SOC socket...')
  fetchBulletScreen()
  setTimeout(fetchData, 1000)
  pollTimer = setInterval(() => { fetchBulletScreen(); setTimeout(fetchData, 1000) }, 10500)
}

const sendToAi = async () => {
  if (!userInput.value.trim() || isAiLoading.value) return
  const text = userInput.value
  chatHistory.value.push({ role: 'user', content: text })
  userInput.value = ''
  isAiLoading.value = true

  try {
    const response = await fetch(`${API_BASE}/chat`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }) })
    const data = await response.json()
    chatHistory.value.push({ role: 'bot', content: data.reply })
  } catch (error) {
    chatHistory.value.push({ role: 'bot', content: '抱歉，服务连接失败，请检查后端状态。' })
  } finally {
    isAiLoading.value = false
    nextTick(() => { const box = document.getElementById('chat-box'); if (box) box.scrollTop = box.scrollHeight })
  }
}

// --- 语音识别相关函数 ---
const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    selectedFile.value = file
  }
}

const clearFile = () => {
  selectedFile.value = null
  asrTranscript.value = ''
  asrAnalysis.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    selectedFile.value = file
  }
}

const handleDragOver = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = () => {
  isDragOver.value = false
}

const handleTranscribe = async () => {
  if (!selectedFile.value || isTranscribing.value) return
  
  isTranscribing.value = true
  asrTranscript.value = ''
  asrAnalysis.value = null
  
  try {
    // 模拟语音识别（实际项目中这里会调用语音识别API）
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟识别结果
    const mockTranscripts = [
      '你这个废物，什么都不会',
      '今天天气真好，心情不错',
      '你怎么这么笨，这么简单的事情都做不好',
      '这首歌真好听，我很喜欢'
    ]
    asrTranscript.value = mockTranscripts[Math.floor(Math.random() * mockTranscripts.length)]
    
    // 调用情感分析API
    const analysisRes = await axios.get(`${API_BASE}/CommentAnalysis`, { params: { sentence: asrTranscript.value }})
    asrAnalysis.value = analysisRes.data
    
  } catch (error) {
    asrTranscript.value = '识别失败，请重试'
    console.error('语音识别失败:', error)
  } finally {
    isTranscribing.value = false
  }
}

const switchModule = (mod) => {
  activeModule.value = mod
  if(mod === 'bilibili') {
    // 不再自动重置房间号，保持用户当前选择的值
    danmakuList.value = [{ time: '--:--:--', nickname: 'SYSTEM', text: '已切换至 B站 数据源' }]
    currentAnalysis.value = null
    startPolling()
  } else if (mod === 'multimodal') {
    // 切换到多模态时，如果雷达图还没初始化，初始化它
    nextTick(() => {
      if(!radarChart && radarChartRef.value) {
        radarChart = echarts.init(radarChartRef.value)
        initRadarChart()
      }
    })
  }
}

const toggleFilterMode = (mode) => {
  filterMode.value = mode
  if(mode === 'filter') {
    pushSysLog('INFO', '异常过滤模式已启用 - 仅显示包含敏感词的弹幕')
  } else {
    pushSysLog('INFO', '全量接入模式已启用 - 显示所有弹幕')
  }
}

const containsSensitiveWord = (text) => {
  return sensitiveWords.some(word => text.includes(word))
}

const simulateSys = () => {
  cpuUsage.value = Math.floor(Math.random() * 20 + 25)
  memUsage.value = Math.floor(Math.random() * 10 + 60)
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  isDark.value = savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)
  
  handleResize(); window.addEventListener('resize', handleResize)
  updateClock(); clockTimer = setInterval(updateClock, 1000)
  sysTimer = setInterval(simulateSys, 2000)
  
  nextTick(() => {
    initCharts()
    updateChartsTheme()
  })
  startPolling()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  clearInterval(pollTimer); clearInterval(clockTimer); clearInterval(sysTimer); clearInterval(hexTimer)
  if(pieChart) pieChart.dispose(); if(lineChart) lineChart.dispose()
  if(monitorPieChart) monitorPieChart.dispose(); if(monitorLineChart) monitorLineChart.dispose(); if(radarChart) radarChart.dispose()
})
</script>

<style scoped>
/* 侧边栏图标悬浮提示 */
.nav-item {
  position: relative; width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
  color: #64748b; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-item:hover { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.dark .nav-item:hover { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.nav-item.active { background: rgba(59, 130, 246, 0.1); color: #3b82f6; box-shadow: inset 3px 0 0 #3b82f6; }
.dark .nav-item.active { background: rgba(6, 182, 212, 0.15); color: #22d3ee; box-shadow: inset 3px 0 0 #22d3ee; }
.nav-tooltip {
  position: absolute; left: 56px; background: #1e293b; color: white; padding: 6px 12px; border-radius: 6px;
  font-size: 12px; opacity: 0; pointer-events: none; transition: opacity 0.2s; white-space: nowrap; font-weight: bold; border: 1px solid #334155;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3); z-index: 50;
}
.nav-item:hover .nav-tooltip { opacity: 1; }

/* 科技面板基础 */
.tech-card {
  background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 20px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04); padding: 24px;
}
.dark .tech-card {
  background: rgba(15, 23, 42, 0.6); border-color: rgba(255, 255, 255, 0.05); box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* 准星角 */
.corner-bracket { position: absolute; width: 10px; height: 10px; border: 2px solid #cbd5e1; transition: border-color 0.3s;}
.tech-card:hover .corner-bracket { border-color: #94a3b8; }
.dark .corner-bracket { border-color: #334155; }
.dark .tech-card:hover .corner-bracket { border-color: #475569; }
.top-left { top: 12px; left: 12px; border-right: none; border-bottom: none; }
.top-right { top: 12px; right: 12px; border-left: none; border-bottom: none; }
.bottom-left { bottom: 12px; left: 12px; border-right: none; border-top: none; }
.bottom-right { bottom: 12px; right: 12px; border-left: none; border-top: none; }

/* 雷达扫描 */
.radar-scan {
  width: 50px; height: 50px; border: 2px dashed #94a3b8; border-radius: 50%; position: relative;
}
.dark .radar-scan { border-color: #334155; }
.radar-scan::after {
  content: ''; position: absolute; width: 50%; height: 50%; background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.3));
  transform-origin: bottom right; animation: scan 2s linear infinite; border-top-right-radius: 100%;
}
.dark .radar-scan::after { background: linear-gradient(45deg, transparent, rgba(6, 182, 212, 0.4)); }
@keyframes scan { to { transform: rotate(360deg); } }

/* 全息图片扫描线特效 */
.animate-hologram-scan {
  animation: hologramScan 1.5s ease-in-out infinite;
}
@keyframes hologramScan {
  0% { transform: translateY(-100%); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(50%); opacity: 0; }
}

.scan-line { position: absolute; top: 0; left: 0; right: 0; height: 20px; animation: scanVertical 3s ease-in-out infinite; pointer-events: none; }
@keyframes scanVertical { 0% { top: -20px; opacity: 0; } 50% { opacity: 1; } 100% { top: 100%; opacity: 0; } }

/* 极简点阵背景 */
.dot-bg { background-image: radial-gradient(#cbd5e1 1px, transparent 1px); background-size: 24px 24px; }
.dark .dot-bg { background-image: radial-gradient(#1e293b 1px, transparent 1px); }

/* 滚动条 */
.tech-scrollbar::-webkit-scrollbar { width: 4px; }
.tech-scrollbar::-webkit-scrollbar-track { background: transparent; }
.tech-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.dark .tech-scrollbar::-webkit-scrollbar-thumb { background: #334155; }

.elegant-scrollbar::-webkit-scrollbar { width: 6px; }
.elegant-scrollbar::-webkit-scrollbar-track { background: transparent; }
.elegant-scrollbar::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.2); border-radius: 10px; }
.elegant-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.4); }
.dark .elegant-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); }

@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
</style>
