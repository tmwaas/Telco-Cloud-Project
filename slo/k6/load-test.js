import http from 'k6/http'; import { sleep } from 'k6';
export const options = { vus: 10, duration: '1m' };
export default function () {
  http.get('http://ran-sim.ns-ran.svc.cluster.local:8000/uplink');
  http.post('http://core-sim.ns-core.svc.cluster.local:8000/session/create', {});
  sleep(1);
}
