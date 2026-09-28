const int HALL_PIN = 2;
const int LED_PIN = 11;

const unsigned long SESSION_TIMEOUT = 60000; // 5000 for testing, 60000 for prod

int prev_hall_state = HIGH;
unsigned long revolution_count = 0;
unsigned long session_start_time = 0;
unsigned long last_revolution_time = 0;
bool session_active = false;

void setup()
{
    pinMode(HALL_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);

    digitalWrite(LED_PIN, LOW);

    Serial.begin(9600);
}

void loop()
{
    int cur_hall_state = digitalRead(HALL_PIN);

    // Detect revolution
    if (prev_hall_state == HIGH && cur_hall_state == LOW)
    {
        unsigned long cur_time = millis();

        // Start a new sesion
        if (!session_active)
        {
            session_active = true;
            session_start_time = cur_time;
            revolution_count = 0;

            digitalWrite(LED_PIN, HIGH);

            Serial.println("Session started");
        }

        revolution_count++;
        last_revolution_time = cur_time;

        Serial.print("Revolutions: ");
        Serial.println(revolution_count);
    }

    // Detect end of session
    if (session_active && millis() - last_revolution_time >= SESSION_TIMEOUT)
    {
        unsigned long elapsed_time = last_revolution_time - session_start_time;

        Serial.print("RUN,");
        Serial.print(revolution_count);
        Serial.print(",");
        Serial.println(elapsed_time);

        session_active = false;
        revolution_count = 0;

        digitalWrite(LED_PIN, LOW);
    }

    prev_hall_state = cur_hall_state;
}
