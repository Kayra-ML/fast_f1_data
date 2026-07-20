import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Gauge, User, Map, Database, Play, ChevronRight, CheckCircle2, ChevronDown, AlertCircle } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { PerformanceChart } from '../components/dashboard/AnalysisCharts';
import { analysisAPI, getEndpointForAnalysis } from '../services/analysisService';

// Data for charts (moved outside to keep component clean)
const telemetryData = Array.from({ length: 100 }, (_, i) => ({
  distance: i * 50,
  speedDriver1: 100 + Math.sin(i / 5) * 150 + Math.random() * 10,
  speedDriver2: 100 + Math.sin(i / 5.2) * 145 + Math.random() * 15,
}));

const sectorTimes = [
  { driver: 'VER', s1: '27.452', s2: '38.120', s3: '22.901', lap: '1:28.473', color: '#3671C6' },
  { driver: 'HAM', s1: '27.510', s2: '38.205', s3: '22.880', lap: '1:28.595', color: '#00A19B' },
  { driver: 'NOR', s1: '27.490', s2: '38.190', s3: '22.950', lap: '1:28.630', color: '#FF8700' },
  { driver: 'LEC', s1: '27.600', s2: '38.150', s3: '22.910', lap: '1:28.660', color: '#E32219' },
];

export function Dashboard() {
  const [step, setStep] = useState(0);
  const [category, setCategory] = useState<string | null>(null);
  const [subCategory, setSubCategory] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState<any[]>([]);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisType, setAnalysisType] = useState<string | null>(null);

  // Endpoint mappings
  const categoryToEndpoint: { [key: string]: { [key: string]: string } } = {
    driver: {
      'SPEED TRACE COMPARISON': 'average-lap-time',
      'TIRE DEGRADATION MODEL': 'consistency',
      'THROTTLE & BRAKE TELEMETRY': 'sector-analysis',
      'PERFORMANCE RANKING': 'performance-ranking',
      'PIT STOP ANALYSIS': 'pit-stop-analysis',
      'POSITION CHANGES': 'position-changes',
    },
    track: {
      'SECTOR TIME ANALYSIS': 'sector-analysis',
      'CORNERING PERFORMANCE': 'average-lap-time',
      'RACE RESULTS': 'race-results',
      'RACE STRATEGY': 'race-strategy',
    },
    general: {
      'AI WIN PROBABILITY': 'season-championship',
      'PIT STOP STRATEGY OPTIMIZATION': 'race-strategy',
      'TEAM PERFORMANCE': 'team-performance-ranking',
      'CIRCUIT PERFORMANCE': 'circuit-performance',
    },
  };

  // Run analysis with backend API
  const runAnalysis = async () => {
    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      if (!category || !subCategory) {
        throw new Error('Category and analysis type required');
      }

      const endpointKey = categoryToEndpoint[category]?.[subCategory];
      if (!endpointKey) {
        throw new Error(`Unknown analysis type: ${subCategory}`);
      }

      setAnalysisType(endpointKey);

      // Call the appropriate API endpoint
      const endpoint = getEndpointForAnalysis(category, endpointKey) as keyof typeof analysisAPI;
      const data = await analysisAPI[endpoint]({ season: 2024, limit: 50, offset: 0 });

      if (Array.isArray(data)) {
        setAnalysisData(data);
      } else {
        setAnalysisError('Unexpected response format');
      }

      setTimeout(() => {
        setIsAnalyzing(false);
        setStep(4);
      }, 1500);
    } catch (error) {
      console.error('Analysis error:', error);
      setAnalysisError(error instanceof Error ? error.message : 'Unknown error');
      setIsAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    setStep(0);
    setCategory(null);
    setSubCategory(null);
  };

  const renderStep0 = () => (
    <motion.div 
      key="step0"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex flex-col items-center justify-center min-h-[60vh] text-center mt-10"
    >
      <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mb-8">
        <Database size={48} className="text-primary" />
      </div>
      <h1 className="font-['Montserrat'] text-4xl md:text-6xl font-black italic uppercase text-on-background tracking-tighter mb-4">
        AI DATA <span className="text-primary">ENGINE</span>
      </h1>
      <p className="text-on-surface-variant font-label-lg uppercase tracking-widest max-w-xl mb-12">
        Initiate a new telemetry query or predictive model forecast.
      </p>
      <button 
        onClick={() => setStep(1)}
        className="px-10 py-5 rounded-full bg-primary text-on-primary font-headline-sm text-headline-sm uppercase tracking-wider hover:bg-primary-fixed btn-glow transition-all duration-300 flex items-center gap-3"
      >
        START NEW ANALYSIS
        <Play size={20} fill="currentColor" />
      </button>
    </motion.div>
  );

  const renderStep1 = () => (
    <motion.div 
      key="step1"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="w-full max-w-4xl mx-auto py-20"
    >
      <h2 className="font-['Montserrat'] text-3xl font-black italic uppercase text-on-background tracking-tighter mb-8 text-center">
        SELECT <span className="text-primary">CATEGORY</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { id: 'driver', title: 'DRIVER ANALYSIS', icon: <User size={32} />, desc: 'Compare telemetry, pace, and tire degradation between drivers.' },
          { id: 'track', title: 'TRACK ANALYSIS', icon: <Map size={32} />, desc: 'Analyze sector times, cornering speeds, and track evolution.' },
          { id: 'general', title: 'GENERAL FORECAST', icon: <Activity size={32} />, desc: 'Overall race pace predictions and AI win probabilities.' }
        ].map(cat => (
          <div 
            key={cat.id}
            onClick={() => { setCategory(cat.id); setStep(2); }}
            className="glass-panel p-8 flex flex-col items-center text-center cursor-pointer hover:border-primary hover:shadow-[0_0_20px_rgba(255,135,0,0.2)] transition-all group"
          >
            <div className="w-16 h-16 bg-surface-container-high rounded-full flex items-center justify-center mb-6 text-on-surface-variant group-hover:text-primary group-hover:bg-primary/10 transition-colors">
              {cat.icon}
            </div>
            <h3 className="font-label-lg font-bold text-on-background mb-3">{cat.title}</h3>
            <p className="text-sm text-on-surface-variant">{cat.desc}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );

  const renderStep2 = () => {
    let subCategories = [];
    if (category === 'driver') {
      subCategories = [
        { id: 'speed', title: 'SPEED TRACE COMPARISON' },
        { id: 'tire', title: 'TIRE DEGRADATION MODEL' },
        { id: 'throttle', title: 'THROTTLE & BRAKE TELEMETRY' }
      ];
    } else if (category === 'track') {
      subCategories = [
        { id: 'sector', title: 'SECTOR TIME ANALYSIS' },
        { id: 'corner', title: 'CORNERING PERFORMANCE' }
      ];
    } else {
      subCategories = [
        { id: 'win', title: 'AI WIN PROBABILITY' },
        { id: 'strategy', title: 'PIT STOP STRATEGY OPTIMIZATION' }
      ];
    }

    return (
      <motion.div 
        key="step2"
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        className="w-full max-w-3xl mx-auto py-20"
      >
        <button onClick={() => setStep(1)} className="text-primary font-bold text-sm uppercase mb-8 hover:underline">&larr; BACK TO CATEGORIES</button>
        <h2 className="font-['Montserrat'] text-3xl font-black italic uppercase text-on-background tracking-tighter mb-8">
          SELECT <span className="text-primary">SPECIFIC ANALYSIS</span>
        </h2>
        <div className="flex flex-col gap-4">
          {subCategories.map(sub => (
            <div 
              key={sub.id}
              onClick={() => { setSubCategory(sub.title); setStep(3); }}
              className="glass-panel p-6 flex items-center justify-between cursor-pointer hover:border-primary hover:bg-primary/5 transition-all group"
            >
              <span className="font-label-lg font-bold text-on-background">{sub.title}</span>
              <ChevronRight className="text-on-surface-variant group-hover:text-primary" />
            </div>
          ))}
        </div>
      </motion.div>
    );
  };

  const renderStep3 = () => (
    <motion.div 
      key="step3"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="w-full max-w-2xl mx-auto py-20 text-center"
    >
      <button onClick={() => setStep(2)} className="text-primary font-bold text-sm uppercase mb-8 hover:underline">&larr; CHANGE SELECTION</button>
      
      <div className="glass-panel p-10 mb-10">
        <h3 className="text-on-surface-variant font-label-md uppercase tracking-widest mb-6">READY TO ANALYZE</h3>
        <div className="flex flex-col items-center gap-4 font-['Montserrat'] text-2xl font-black italic uppercase text-on-background">
          <span>{category === 'driver' ? 'DRIVER ANALYSIS' : category === 'track' ? 'TRACK ANALYSIS' : 'GENERAL FORECAST'}</span>
          <ChevronDown size={24} className="text-primary" />
          <span className="text-primary">{subCategory}</span>
        </div>
      </div>

      {!isAnalyzing ? (
        <button 
          onClick={runAnalysis}
          className="px-12 py-5 rounded-full bg-on-background text-background font-headline-sm text-headline-sm uppercase tracking-wider hover:bg-primary hover:text-on-primary btn-glow transition-all duration-300 w-full"
        >
          RUN ANALYSIS NOW
        </button>
      ) : (
        <div className="flex flex-col items-center justify-center p-8 bg-surface-container-high/30 rounded-xl border border-outline-variant">
          <div className="w-12 h-12 border-4 border-outline-variant border-t-primary rounded-full animate-spin mb-6"></div>
          <p className="font-label-lg text-primary font-bold animate-pulse">PROCESSING TELEMETRY DATA...</p>
        </div>
      )}
    </motion.div>
  );

  const renderStep4 = () => (
    <motion.div 
      key="step4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-7xl mx-auto space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-8">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle2 className="text-tertiary" />
            <span className="text-tertiary font-bold text-sm uppercase tracking-widest">ANALYSIS COMPLETE</span>
          </div>
          <h1 className="font-['Montserrat'] text-3xl md:text-4xl font-black italic uppercase text-on-background tracking-tighter mb-2">
            {subCategory}
          </h1>
        </div>
        
        <button 
          onClick={resetAnalysis}
          className="bg-surface-container-high text-on-background border border-outline-variant px-6 py-2 rounded-md font-label-sm font-bold uppercase hover:bg-white hover:border-primary transition-all"
        >
          NEW ANALYSIS
        </button>
      </div>

      {/* Error message */}
      {analysisError && (
        <div className="glass-panel p-4 border border-error/50 bg-error/10 flex items-center gap-3">
          <AlertCircle className="text-error" size={20} />
          <p className="text-error font-label-md">{analysisError}</p>
        </div>
      )}

      {/* Visualizations based on selection */}
      {!analysisError && analysisData.length > 0 && analysisType && (
        <PerformanceChart 
          data={analysisData}
          analysisType={analysisType}
          title={subCategory || 'Analysis Results'}
        />
      )}

      {!analysisError && analysisData.length === 0 && (
        <div className="glass-panel p-8 text-center">
          <p className="text-on-surface-variant font-label-lg">No data available for this analysis</p>
        </div>
      )}
    </motion.div>
  );

  return (
    <div className="pt-24 pb-12 px-4 md:px-margin-desktop bg-background min-h-screen">
      <AnimatePresence mode="wait">
        {step === 0 && renderStep0()}
        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
        {step === 4 && renderStep4()}
      </AnimatePresence>
    </div>
  );
}
