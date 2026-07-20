import os
from dotenv import load_dotenv
from worker.loaders.f1_postgres_loader import F1PostgresLoader
from worker.processors.data_cleaner import DataCleaner
from worker.collectors.session_collector import SessionCollector
from worker.collectors.driver_collector import DriverCollector
from worker.collectors.position_collector import PositionCollector
from worker.collectors.pit_stop_collector import PitStopCollector
from worker.collectors.lap_collector import LapCollector
from worker.collectors.session_results_collector import SessionResultsCollector
from worker.collectors.race_control_collector import RaceControlCollector


def main():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    loader = F1PostgresLoader(db_url)
    cleaner = DataCleaner(db_url)
    session_collector = SessionCollector(db_url)
    driver_collector = DriverCollector(db_url)
    position_collector = PositionCollector(db_url)
    pit_collector = PitStopCollector(db_url)
    lap_collector = LapCollector(db_url)
    results_collector = SessionResultsCollector(db_url)
    race_control_collector = RaceControlCollector(db_url)

    print("F1 veri yükleme işlemi başlatılıyor...")
    loader.load_all()

    print("Veri temizleme işlemi başlatılıyor...")
    cleaner.clean_all()

    print("Worker kolektörleri çalıştırılıyor...")
    session_collector.collect_session_summary()
    driver_collector.collect_driver_rankings()
    position_collector.collect_grid_to_finish()
    pit_collector.collect_pit_stop_stats()
    lap_collector.collect_lap_summary()
    results_collector.collect_race_results_summary()
    race_control_collector.collect_status_overview()

    print("Worker işlemleri tamamlandı.")


if __name__ == "__main__":
    main()
