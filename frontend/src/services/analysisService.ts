// API service for backend communication
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface AnalysisParams {
  season?: number;
  driver_id?: string;
  driver_number?: number;
  constructor_id?: string;
  circuit_id?: string;
  limit?: number;
  offset?: number;
}

export const analysisAPI = {
  // Driver endpoints
  getDriverPerformance: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/driver/performance-ranking?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getDriverAverageLapTime: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/driver/average-lap-time?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getDriverSectorAnalysis: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/driver/sector-analysis?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getDriverConsistency: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/driver/consistency?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getDriverPitStops: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/driver/pit-stop-analysis?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getDriverPositionChanges: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/driver/position-changes?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  // Team endpoints
  getTeamPerformance: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/team/performance-ranking?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getTeamConsistency: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/team/consistency?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  // Circuit endpoints
  getCircuitPerformance: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/circuit/performance?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  // Race endpoints
  getRaceResults: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/race/results?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  getRaceStrategy: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/race/strategy?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
  
  // Season endpoints
  getSeasonChampionship: (params: AnalysisParams) =>
    fetch(`${API_BASE_URL}/analysis/season/championship?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)]))}`)
      .then(r => r.json()),
};

export const getEndpointForAnalysis = (category: string, analysisType: string): keyof typeof analysisAPI => {
  const endpoints: { [key: string]: keyof typeof analysisAPI } = {
    'driver_performance-ranking': 'getDriverPerformance',
    'driver_average-lap-time': 'getDriverAverageLapTime',
    'driver_sector-analysis': 'getDriverSectorAnalysis',
    'driver_consistency': 'getDriverConsistency',
    'driver_pit-stop-analysis': 'getDriverPitStops',
    'driver_position-changes': 'getDriverPositionChanges',
    'team_performance-ranking': 'getTeamPerformance',
    'team_consistency': 'getTeamConsistency',
    'circuit_performance': 'getCircuitPerformance',
    'race_results': 'getRaceResults',
    'race_strategy': 'getRaceStrategy',
    'season_championship': 'getSeasonChampionship',
  };
  
  return endpoints[`${category}_${analysisType}`] || 'getDriverPerformance';
};
