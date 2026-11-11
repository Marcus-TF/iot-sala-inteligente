const net = require('net');
const { Aedes } = require('aedes');

(async () => {
  const aedes = await Aedes.createBroker();
  net.createServer(aedes.handle).listen(1883, () => console.log('broker em 1883'));
})();
