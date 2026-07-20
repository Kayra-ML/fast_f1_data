export function Footer() {
  return (
    <footer className="w-full py-margin-desktop px-margin-desktop flex flex-col md:flex-row justify-between items-center gap-4 bg-surface-container-lowest border-t border-white/5">
      <div className="font-headline-sm text-headline-sm text-primary uppercase">
        F1 ANALYTIX
      </div>
      <p className="font-label-sm text-label-sm text-on-surface-variant uppercase">
        © 2024 F1 ANALYTIX. ALL RIGHTS RESERVED.
      </p>
      <div className="font-label-sm text-label-sm text-on-surface-variant uppercase text-center md:text-right max-w-sm">
        DIVE DEEPER INTO DETAILED RACE FORECASTS AND HISTORIC MODEL INSIGHTS.
      </div>
    </footer>
  );
}
