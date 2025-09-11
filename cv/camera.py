import cv2
from cv.detector import HandDetector
import time

class GestureCamera:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Não foi possível abrir a webcam.")

        self.detector = HandDetector()
        self.current_game_state = "tela_inicial"

    def run(self):

        while True:
            success, img = self.cap.read()
            if not success:
                break

            img = cv2.flip(img, 1)
            img = self.detector.find_hands(img)
            lm_list = self.detector.get_landmarks(img)

            gesture = self.detector.recognize_gesture(lm_list)

            actionable_gesture = self.detector.check_continuous_gesture(gesture, duration=2)

            if actionable_gesture:
                self.handle_actions(actionable_gesture)

            # Lógica para o gesto de fechar a mão (MAO_ABERTA > PUNHO)
            self.handle_hand_close(gesture)

            self.display_info(img, gesture)

            cv2.imshow("Game Control", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def handle_hand_close(self, current_gesture):

        if not hasattr(self, 'previous_gesture'):
            self.previous_gesture = None

        if self.current_game_state == "fase":
            if self.previous_gesture == "MAO_ABERTA" and current_gesture == "PUNHO":
                print("AÇÃO: Lógica booleana validada! (Mão fechou)")

        self.previous_gesture = current_gesture

    def handle_actions(self, gesture):

        print(f"Gesto '{gesture}' reconhecido por 2 segundos no estado '{self.current_game_state}'")

        if self.current_game_state == "tela_inicial":
            if gesture == "ROCK":
                print("AÇÃO: INICIANDO JOGO...")
                self.current_game_state = "fase"
            elif gesture == "PUNHO":
                print("AÇÃO: VENDO TUTORIAL...")
                self.current_game_state = "tutorial"
            elif gesture == "PAZ":
                print("AÇÃO: SAINDO DO JOGO...")
                exit()

        elif self.current_game_state == "tutorial":
            if gesture == "PAZ":
                print("AÇÃO: VOLTANDO AO MENU INICIAL...")
                self.current_game_state = "tela_inicial"

        elif self.current_game_state == "fase":
            if gesture == "PAZ":
                print("AÇÃO: VOLTANDO AO MENU INICIAL...")
                self.current_game_state = "tela_inicial"
            elif gesture == "UM":
                print("AÇÃO: REPETINDO NARRAÇÃO...")

    def display_info(self, img, gesture):

        h, w, _ = img.shape

        cv2.rectangle(img, (0, 0), (w, 80), (20, 20, 20), -1)


        cv2.putText(img, f"ESTADO: {self.current_game_state.upper()}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


        detected_gesture = gesture if gesture else "Nenhum"
        cv2.putText(img, f"Gesto: {detected_gesture}", (20, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)