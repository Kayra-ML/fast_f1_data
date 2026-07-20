import { ResponsiveContainer, BarChart, Bar, LineChart, Line, AreaChart, Area, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Activity, TrendingUp } from 'lucide-react';

interface ChartProps {
  data: any[];
  analysisType: string;
  title: string;
}

export function PerformanceChart({ data, analysisType, title }: ChartProps) {
  // Format: [{driver: 'VER', wins: 5, podiums: 15, dnf_rate: 8.5}, ...]
  const COLORS = ['#3671C6', '#00A19B', '#FF8700', '#E32219', '#1d9dce'];

  if (analysisType === 'performance-ranking') {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <TrendingUp size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
              <Legend />
              <Bar dataKey="wins" fill="#FF6B6B" name="Wins" />
              <Bar dataKey="podiums" fill="#4ECDC4" name="Podiums" />
              <Bar dataKey="races" fill="#95E1D3" name="Total Races" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'average-lap-time') {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <Activity size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} formatter={(value: any) => `${value?.toFixed(3)}s`} />
              <Legend />
              <Line type="monotone" dataKey="avg_lap_time" stroke="#3671C6" strokeWidth={2} name="Avg Lap Time" dot={{ r: 4 }} />
              <Line type="monotone" dataKey="best_lap_time" stroke="#FF8700" strokeWidth={2} name="Best Lap" dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'sector-analysis') {
    // Format: [{driver_number: 1, avg_s1: 27.4, avg_s2: 38.1, avg_s3: 22.9}, ...]
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <Activity size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} formatter={(value: any) => `${value?.toFixed(3)}s`} />
              <Legend />
              <Bar dataKey="avg_s1" fill="#3671C6" name="Sector 1" />
              <Bar dataKey="avg_s2" fill="#FF8700" name="Sector 2" />
              <Bar dataKey="avg_s3" fill="#00A19B" name="Sector 3" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'consistency') {
    // Format: [{driver_number: 1, avg_lap_time: 88.5, lap_variance: 2.3}, ...]
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <Activity size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis yAxisId="left" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis yAxisId="right" orientation="right" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} formatter={(value: any) => `${value?.toFixed(3)}`} />
              <Legend />
              <Bar yAxisId="left" dataKey="avg_lap_time" fill="#3671C6" name="Avg Lap Time" />
              <Bar yAxisId="right" dataKey="lap_variance" fill="#FF6B6B" name="Variance (StdDev)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'pit-stop-analysis') {
    // Format: [{driver_number: 1, total_stops: 2, avg_stop_duration: 28.5}, ...]
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <Activity size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} formatter={(value: any) => `${value?.toFixed(2)}s`} />
              <Legend />
              <Bar dataKey="avg_stop_duration" fill="#FF8700" name="Avg Stop Duration (s)" />
              <Bar dataKey="total_stops" fill="#3671C6" name="Total Stops" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'position-changes') {
    // Format: [{session_key: ..., driver_number: 1, grid_position: 3, finish_position: 1}, ...]
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <Activity size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <defs>
                <linearGradient id="colorGrid" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3671C6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#3671C6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorFinish" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#FF8700" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#FF8700" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
              <Legend />
              <Area type="monotone" dataKey="grid_position" stroke="#3671C6" fillOpacity={1} fill="url(#colorGrid)" name="Grid Position" />
              <Area type="monotone" dataKey="finish_position" stroke="#FF8700" fillOpacity={1} fill="url(#colorFinish)" name="Finish Position" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'team-performance-ranking') {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <TrendingUp size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="constructor_id" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
              <Legend />
              <Bar dataKey="wins" fill="#FF6B6B" name="Wins" />
              <Bar dataKey="podiums" fill="#4ECDC4" name="Podiums" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'season-championship') {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <TrendingUp size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="driver_number" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 11}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
              <Legend />
              <Bar dataKey="total_points" fill="#3671C6" name="Total Points" />
              <Bar dataKey="wins" fill="#FF8700" name="Wins" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (analysisType === 'race-results') {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <Activity size={20} className="text-primary" />
          <h3 className="font-label-lg font-bold text-on-background uppercase">{title}</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-outline-variant">
                <th className="text-left py-3 px-4 font-bold text-on-background">Driver</th>
                <th className="text-center py-3 px-4 font-bold text-on-background">Position</th>
                <th className="text-center py-3 px-4 font-bold text-on-background">Laps</th>
                <th className="text-center py-3 px-4 font-bold text-on-background">Duration</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx} className="border-b border-surface-container-high hover:bg-surface-container-high/50 transition-colors">
                  <td className="py-3 px-4 font-label-md text-on-background">{row.driver_number}</td>
                  <td className="text-center py-3 px-4 text-on-surface-variant">{row.position}</td>
                  <td className="text-center py-3 px-4 text-on-surface-variant">{row.number_of_laps}</td>
                  <td className="text-center py-3 px-4 text-on-surface-variant">{row.duration}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  // Fallback table view
  return (
    <div className="glass-panel p-6">
      <h3 className="font-label-lg font-bold text-on-background uppercase mb-6">{title}</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-outline-variant">
              {data.length > 0 && Object.keys(data[0]).map(key => (
                <th key={key} className="text-left py-3 px-4 font-bold text-on-background">{key.toUpperCase()}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} className="border-b border-surface-container-high hover:bg-surface-container-high/50">
                {Object.values(row).map((val, vidx) => (
                  <td key={vidx} className="py-3 px-4 text-on-surface-variant">{String(val)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AnalysisCharts;
