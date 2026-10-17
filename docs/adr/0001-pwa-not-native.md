# PWA instead of a native iOS app

The app is a single React + Vite Progressive Web App, installed on the iPhone via "Add to Home Screen". The same build serves the phone logging views and the wider-screen dashboard. A native app (Expo or Swift) needs either a Mac or the paid Apple Developer Program for a usable install, and the project has neither: it runs at £0 and is built on Windows. Expo Go was rejected because the app would always run inside Expo Go and break with Expo SDK upgrades.

## Consequences

- No live Apple Health / HealthKit access. (Amended 2026-10-17: Watch Data was dropped, see ADR-0008.)
- iOS web push only works from the home-screen app (iOS 16.4+), so any notifications are best-effort.
