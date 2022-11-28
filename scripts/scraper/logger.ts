import util from 'util';
import winston, { createLogger, format } from 'winston';

const combineMessageAndSplat = () => {
  return {
    // @ts-ignore
    transform: info => {
      info.message = util
        .format(info.message, ...(info[Symbol.for('splat')] || []))
        .replaceAll(/\s+/g, ' ');
      return info;
    }
  };
};

export const getLogger = () => {
  return createLogger({
    level: 'info',
    transports: [
      new winston.transports.Console({
        format: format.combine(
          format(info => {
            info.level = info.level.toUpperCase();
            return info;
          })(),
          format.colorize(),
          format.timestamp(),
          combineMessageAndSplat(),
          format.printf(
            info => `${info.timestamp} ${info.level}: ${info.message}`
          )
        )
      }),
      new winston.transports.File({
        filename: 'logs/access.log',
        level: 'info',
        format: format.combine(
          format(info => {
            info.level = info.level.toUpperCase();
            return info;
          })(),
          format.timestamp(),
          combineMessageAndSplat(),
          format.printf(
            info => `${info.timestamp} ${info.level}: ${info.message}`
          )
        )
      })
    ]
  });
};
