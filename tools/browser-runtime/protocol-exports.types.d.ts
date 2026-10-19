export { ArchkeelGraphProtocol, ArchkeelGraphSceneProtocol };
declare global {
  interface Window {
    ArchkeelGraphScene: typeof import("./report-graph-scene.js");
    ArchkeelAtlasDeviations: typeof import("./report-atlas-deviations.js");
  }
}
