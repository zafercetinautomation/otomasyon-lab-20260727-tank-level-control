PROGRAM MAIN
VAR
    // Eğitim amaçlı sembolik girişler
    bAutoMode        : BOOL := TRUE;
    bStart           : BOOL;
    bStop            : BOOL;
    bLowLevelSensor  : BOOL;
    bHighLevelSensor : BOOL;
    bResetAlarm      : BOOL;

    // Çıkışlar ve izlenebilir durumlar
    bInletValve      : BOOL;
    bTankFull        : BOOL;
    bSensorFault     : BOOL;
    bCycleEnabled    : BOOL;
    bFillRequest     : BOOL;
    bSensorInvalid   : BOOL;

    fbStart          : R_TRIG;
    fbReset          : R_TRIG;
END_VAR

fbStart(CLK := bStart);
fbReset(CLK := bResetAlarm);

// Üst sensör sıvı görürken alt sensörün görmemesi fiziksel olarak tutarsızdır.
bSensorInvalid := bHighLevelSensor AND NOT bLowLevelSensor;

IF bSensorInvalid THEN
    bSensorFault := TRUE;
END_IF

// Stop ve otomatik modun kapanması her zaman dolumu durdurur.
IF bStop OR NOT bAutoMode THEN
    bCycleEnabled := FALSE;
    bFillRequest := FALSE;
END_IF

// Alarm yalnızca sensörler tutarlı ve çevrim durmuşken sıfırlanabilir.
IF fbReset.Q AND NOT bSensorInvalid AND NOT bCycleEnabled THEN
    bSensorFault := FALSE;
END_IF

// Yeni çevrim, alarm yokken başlatılır.
IF fbStart.Q AND bAutoMode AND NOT bSensorFault THEN
    bCycleEnabled := TRUE;
    bFillRequest := NOT bHighLevelSensor;
END_IF

IF bSensorFault THEN
    bCycleEnabled := FALSE;
    bFillRequest := FALSE;
ELSIF bCycleEnabled THEN
    // Üst seviye dolumu bitirir.
    IF bHighLevelSensor THEN
        bFillRequest := FALSE;
    // Yeni dolum yalnızca seviye alt sensörün de altına düştüğünde başlar.
    ELSIF NOT bLowLevelSensor THEN
        bFillRequest := TRUE;
    END_IF
END_IF

bTankFull := bHighLevelSensor AND bLowLevelSensor AND NOT bSensorFault;
bInletValve := bAutoMode
    AND bCycleEnabled
    AND bFillRequest
    AND NOT bHighLevelSensor
    AND NOT bSensorFault;

// Gerçek bir tesiste bağımsız taşma koruması, vana geri bildirimi,
// zaman aşımı ve sertifikalı emniyet fonksiyonları ayrıca tasarlanmalıdır.
