import React, { useState } from 'react';
import { Sparkles, ArrowRight, Copy, Check, Loader2, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface TranslationResult {
  translation: string;
  keywords: string[];
}

function App() {
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TranslationResult | null>(null);
  const [copied, setCopied] = useState(false);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    setResult(null); // Reset result on new request

    try {
        // Real API call
        const response = await fetch('/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: inputText }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        setResult(data);
    } catch (error) {
      console.error("Translation failed", error);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (result) {
      navigator.clipboard.writeText(result.translation);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-[#f5f5f7] flex flex-col items-center justify-center p-4 sm:p-8 font-sans selection:bg-blue-100 selection:text-blue-900 overflow-hidden relative">
      
      {/* Background Decorative Elements */}
      <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-400/20 rounded-full blur-[120px] pointer-events-none mix-blend-multiply opacity-70" />
      <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-400/20 rounded-full blur-[120px] pointer-events-none mix-blend-multiply opacity-70" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }} // Apple-like ease
        className="w-full max-w-5xl z-10 flex flex-col items-center"
      >
        {/* Header */}
        <header className="mb-12 text-center space-y-6">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/60 border border-white/60 backdrop-blur-xl shadow-sm mb-2 hover:bg-white/80 transition-colors cursor-default"
          >
            <Sparkles className="w-3.5 h-3.5 text-blue-500 fill-blue-500/20" />
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest">AI Translator v1.0</span>
          </motion.div>
          
          <div className="space-y-2">
            <h1 className="text-4xl sm:text-6xl font-semibold tracking-tight text-slate-900">
              Break Language <br className="hidden sm:block" />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-600 animate-gradient-x">Barriers</span>
            </h1>
          </div>
        </header>

        {/* Main Interface */}
        <div className="w-full grid grid-cols-1 lg:grid-cols-2 gap-6 relative">
          
          {/* Input Section */}
          <motion.div 
            className="group relative flex flex-col h-[420px] bg-white/60 backdrop-blur-2xl rounded-[32px] border border-white/60 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden transition-all duration-500 hover:shadow-[0_20px_40px_rgb(0,0,0,0.06)] hover:bg-white/70"
          >
            <div className="p-8 flex-1 flex flex-col">
              <div className="flex justify-between items-center mb-6">
                <label htmlFor="input" className="text-xs font-bold text-slate-400 uppercase tracking-widest">Input (Chinese)</label>
              </div>
              <textarea
                id="input"
                className="flex-1 w-full bg-transparent border-none resize-none focus:ring-0 text-2xl text-slate-800 placeholder:text-slate-300 leading-normal p-0 font-medium"
                placeholder="在此输入文本..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                spellCheck={false}
              />
            </div>
            
            <div className="p-6 border-t border-slate-100/50 bg-white/20 flex justify-between items-center">
               <div className="text-xs text-slate-400 font-medium px-3 py-1.5 rounded-full bg-slate-100/50">
                 {inputText.length} characters
               </div>
               <button 
                onClick={handleTranslate}
                disabled={isLoading || !inputText.trim()}
                className="relative overflow-hidden rounded-2xl bg-slate-900 text-white pl-6 pr-5 py-3.5 font-medium transition-all duration-300 hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95 flex items-center gap-2 group/btn shadow-lg shadow-slate-900/20"
               >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Processing</span>
                    </>
                  ) : (
                    <>
                      <span>Translate</span>
                      <ArrowRight className="w-4 h-4 transition-transform group-hover/btn:translate-x-1" />
                    </>
                  )}
               </button>
            </div>
          </motion.div>

          {/* Output Section */}
          <motion.div 
            className="relative flex flex-col h-[420px] bg-white/40 backdrop-blur-2xl rounded-[32px] border border-white/60 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden"
          >
             <div className="p-8 flex-1 flex flex-col">
              <div className="flex justify-between items-center mb-6">
                 <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Result (English)</label>
                 <AnimatePresence>
                   {result && (
                     <motion.button 
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      onClick={copyToClipboard}
                      className="p-2 rounded-full hover:bg-white/60 transition-colors text-slate-500 hover:text-slate-900 active:scale-90"
                      title="Copy translation"
                     >
                       {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
                     </motion.button>
                   )}
                 </AnimatePresence>
              </div>
              
              <div className="flex-1 relative">
                <AnimatePresence mode="wait">
                  {isLoading ? (
                    <motion.div 
                      key="loading"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="absolute inset-0 flex items-center justify-center"
                    >
                      <div className="flex flex-col items-center gap-4">
                         <div className="relative">
                           <div className="w-16 h-16 rounded-full border-4 border-slate-100 opacity-30" />
                           <div className="absolute inset-0 w-16 h-16 rounded-full border-4 border-t-blue-500 border-r-transparent border-b-transparent border-l-transparent animate-spin" />
                         </div>
                         <p className="text-sm font-medium text-slate-400 animate-pulse">AI is thinking...</p>
                      </div>
                    </motion.div>
                  ) : result ? (
                    <motion.div
                      key="result"
                      initial={{ opacity: 0, y: 10, filter: 'blur(10px)' }}
                      animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
                      transition={{ duration: 0.5, ease: "easeOut" }}
                      className="h-full flex flex-col"
                    >
                      <p className="text-2xl text-slate-800 leading-relaxed font-medium">
                        {result.translation}
                      </p>
                      
                      <div className="mt-auto pt-8">
                        <div className="flex items-center gap-2 mb-4">
                          <Zap className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
                          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Key Insights</span>
                        </div>
                        <div className="flex flex-wrap gap-2.5">
                          {result.keywords.map((keyword, i) => (
                            <motion.span 
                              key={i}
                              initial={{ opacity: 0, scale: 0.8 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ delay: i * 0.1 }}
                              className="px-3.5 py-1.5 rounded-lg bg-white/40 border border-white/60 text-sm font-medium text-slate-600 shadow-sm backdrop-blur-sm"
                            >
                              {keyword}
                            </motion.span>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  ) : (
                    <motion.div 
                      key="empty"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="absolute inset-0 flex flex-col items-center justify-center text-slate-300"
                    >
                      <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
                        <Sparkles className="w-8 h-8 text-slate-200" />
                      </div>
                      <p className="font-medium">Translation will appear here</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Footer */}
        <footer className="mt-20 text-center">
          <p className="text-sm text-slate-400 font-medium">Designed for AITranslator</p>
        </footer>

      </motion.div>
    </div>
  );
}

export default App;
