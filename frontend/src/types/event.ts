export interface Event {
  id: number;
  title: string;
  description: string;
  company: {
    name: string;
    logo: string;
  };
  endDate: string;
  solutions: {
    current: number;
    total: number;
  };
}
