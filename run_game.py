import pygame
import TicTacToeController
import TicTacToeView
import TicTacToeModel

def main():
    view = TicTacToeView.TicTacToeView()
    model = TicTacToeModel.TicTacToeModel()
    controller = TicTacToeController.TicTacToeController(view, model)

    pygame.display.update()
    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(30)
        pygame.display.update()
        done = controller.process_click_event(view, model)
        controller.update_grid_view(view, model)
        if done:
            pygame.quit()

if __name__ == '__main__':
    main()