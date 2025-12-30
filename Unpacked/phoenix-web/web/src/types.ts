export type ChakraMode =
  | "ROOT"
  | "SACRAL"
  | "SOLAR"
  | "HEART"
  | "THROAT"
  | "THIRD_EYE"
  | "CROWN";

export interface IVPScore {
  clarity: number;
  depth: number;
  actionability: number;
  alignment: number;
  emergence: number;
}

export interface PhoenixResponse {
  plainSummary: string;
  detailed: string;
  ivp: IVPScore;
  activeLayers: string[];
  chakra: ChakraMode;
  cycles: number;
  timestamp: string;
}